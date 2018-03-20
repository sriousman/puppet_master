"""
Python utilities for reading and writing MKEYED files

@author: Troy & Timothy Farrell
@author: Equity Insurance Group
"""

import struct
from bisect import bisect_left
from collections import namedtuple
from struct import unpack
from subprocess import Popen, PIPE
from bbpy.util import convIntFromString
from bbpy import strings

PRO5 = "/usr/local/basis/pro5/pro5"
PRO5CONFIG = "bbw.config"

# Filetype definitions

FT_INDEXED = 0
FT_SERIAL = 1
FT_KEYED = 2
FT_STRING = 3
FT_PROGRAM = 4
FT_DIRECTORY = 5
FT_MKEYED = 6
FT_CISAM = 7
FT_MKEYED4GB = 102

filetypes = (
    "INDEXED", "SERIAL", "KEYED", "STRING", "PROGRAM", "DIRECTORY",
    "MKEYED", "CISAM")
filetype_by_id = dict([(i, f) for i, f in enumerate(filetypes)])
filetype_by_id[FT_MKEYED4GB] = 'MKEYED-4GB'


def log(fmt, *args, **kwargs):
    """Print debug messages"""
    # print(fmt.format(*args, **kwargs))
    pass


class MKEYEDReader(object):
    """Reader for MKEYED data files

    This module is mostly abstracted with L{template} module, you'll almost
    always want to use it instead.

    :ivar keynum: In "Multi-KEYED" files, you can have multiple keys (even
        though we typically only use one so this is typically 0).  keynum
        specifies which key we are referring to.
    :ivar keys: A list (typically holding only 1) of the keyfield
        descriptions for a record (L{MKEYEDKeyFieldDefinition}).  In SQL terms,
        each item in this list is a member of a primary key.  But since we
        are using BBx records, it contains each definition uses the offset
        and length of the key field data.
    :ivar _currentkey: The last key returned.
    :ivar _cursor_spec: The parameters used to initialize the cursor
    :ivar _cursor: A read cursor that will return the next key, record
    :ivar _filelength: The length of the file in bytes (not currently used)
    :ivar _indexblocks: A list of the file offsets (addresses) of the
        index blocks
    :ivar _keycount: The number of keys in the MKEYED file, should == len(keys)
    :ivar _keysize: The size in characters of a record key, this is not always
        accurate.  Use self.getKeylength() to always get the accurate keysize.
    :ivar _nextaddr: The offset of where the next record will go. (Not
        currently used).
    :ivar _recordcount: The total number of records in an MKEYED file
        In the case of an MKEYED file, the normal file header has a value
        of "0".  The proper value is retrieved from the MKEYED header.
    :ivar _recordsize: The total size in bytes of a record
    :ivar _type: The filetype of the data file opened (should be FT_MKEYED)

    :group Public Methods: open, close, find, read*, getStats, getKeylength
    :group Support Methods: next, __*__, _set*, _split*, _*MKEYED*, _check*,
        _readFileHeader
    """

    # Python support methods

    def __init__(self, f, mode="rb"):
        """\
        Build an L{MKEYEDReader} instance.  The instance can be used to read
        records from an MKEYED file.

        :param f: The full path to a BBx data file or an open file object.
          (i.e. "/usr/HTTPServer/data/ELFSUS")
        :param mode: Allows the programmer to specify what mode to open the
            file in.

        :return: Instance of a L{MKEYEDReader}.
        """

        # Initialize our values
        self.keynum = None
        self._currentkey = None
        self._cursor_spec = None
        self._cursor = None
        self._type = -1
        self._recordcount = 0
        self._recordsize = 0
        self._addressexclusions = set()
        self._constants = {}
        self._indexes = {}

        # Open the BBx Data file
        self.open(f, mode)

        # Read the useful info
        self._readFileHeader()

    def __iter__(self):
        """Support Python iteration"""
        self._cursor, self._cursor_spec = None, None
        return self  # This works because self.next() works

    def __len__(self):
        """Return the number of records in the file"""
        return self._recordcount

    def __del__(self):
        """\
        Whenever the L{MKEYEDReader} instance is deleted, close any open file
        handles.
        """

        if self._f:
            self.close()

    # Public methods
    def readAll(
            self, key="", keynum=None, field=0, numerics=False,
            stripzeros=False):
        """
        Read all records matching the key.

        ReadAll returns a list of all records with partial or full matches to
        the supplied key. Passing no key or a key=="" will RETURN ALL RECORDS
        in the file.  This can be slow, consider yourself warned.

        :param key: The key of the record you are searching for.  If this is
            left blank (None), then the cursor will return the next key
        :param keynum: Keynum refers to which key in an MKEYED file the key
            should be searched on.
        :param field: field specifies the field of the record to return, this
            is for numerics
        :param numerics: Specifies if numerics should be returned with the
            string record.  If True, then the L{field} parameter is ignored.
        :return: A list of records that start with the key passed or if
            L{field} is specified, then that specific field.
        :raises BBPyKeyNotFoundError: BBPyKeyNotFoundError if key is not found
        """

        recs = []
        data = None

        try:
            data = self.readRecord(
                key, keynum, stripzeros=stripzeros, readAll=True)
        except BBPyPartialKeyFoundException as e:
            data = self.readRecord(
                e.recordkey, keynum, stripzeros=stripzeros, readAll=True)

        done = False
        while not done:
            if not numerics:
                recs.append(data[1][field])
            else:
                recs.append(data[1])
            try:
                data = self.readRecord(stripzeros=stripzeros, readAll=True)
                if not data[0][0].startswith(key):
                    done = True
            except (BBPyKeyNotFoundError, MKEYEDReaderEOF):
                done = True
        return recs

    def readGenerator(
            self, key=None, keynum=None, field=0, numerics=False,
            stripzeros=False):
        """
        Create a read generator.
        :param field: field specifies the field of the record to return, this
            is for numerics
        :param numerics: Specifies if numerics should be returned with the
            string record.  If True, then the L{field} parameter is ignored.
        :return: A generator
        """
        data = self.readRecord(
            key=key, keynum=keynum, stripzeros=stripzeros, readAll=True)
        while data:
            if not numerics:
                yield data[1][field]
            else:
                yield data[1]
            try:
                data = self.readRecord(stripzeros=stripzeros, readAll=True)
            except (BBPyKeyNotFoundError, MKEYEDReaderEOF):
                raise StopIteration

    def find(self, key=None, keynum=None, field=0):
        """\
        find() acts just like read() with one exception.  Current key pointer
        is only updated if a full key is matched, while read() will
        change it regardless of a successful key find.

        :note: find() only modifies the current key pointer on a successful key
            match.
        :param key: The key of the record you are searching for.  If this is
            left blank (None) then the cursor will return the next key
        :param keynum: Keynum refers to which key in an MKEYED file the key
            should be searched on.
        :param field: field specifies the field of the record to return, this
            is for numerics
        :return: The first field for the record that matches the key passed or
            if L{field} is specified, then that specific field.
        :raises BBPyKeyNotFoundError: BBPyKeyNotFoundError if key is not found
        :raises BBPyPartialKeyFoundException: BBPyPartialKeyFoundException if
            a partial key is found
        """
        tempkey = self._currentkey
        tempspec = self._cursor_spec
        try:
            return self.read(key, keynum, field)
        except (BBPyPartialKeyFoundException, BBPyKeyNotFoundError) as e:
            self._cursor, self._cursor_spec = None, None
            self.read(tempkey, keynum)
            self._cursor_spec = tempspec
            raise e

    def read(self, key=None, keynum=None, field=0):
        """Return a specific field of record data.

        :note: read() modifies the current key pointer.
        :param key: The key of the record you are searching for.  If this is
            left blank (None) then the cursor will return the next key
        :param keynum: Keynum refers to which key in an MKEYED file the key
            should be searched on.
        :param field: field specifies the field of the record to return, this
            is for numerics
        :return: The first field for the record that matches the key passed or
            if field is specified, then that specific field.
        :raises BBPyKeyNotFoundError: BBPyKeyNotFoundError if key is not found
        :raises BBPyPartialKeyFoundException: BBPyPartialKeyFoundException if
            only a partial key is found
        """
        result = self.readRecord(key, keynum)
        return result[field]

    # Parameters when a cursor is initialized
    CursorSpec = namedtuple(
        'CursorSpec', ['key', 'keynum', 'stripzeros', 'readAll', 'nonumerics'])

    def readRecord(
            self, key=None, keynum=None, stripzeros=False, readAll=False,
            nonumerics=False):
        """\
        Return record data as a tuple of fields

        :note: readRecord() modifies the current key pointer.
        :param key: The key of the record you are searching for.  If this is
            left blank (None) then the cursor will return the next key
        :param keynum: Keynum refers to which key in an MKEYED file the key
            should be searched on.
        :param stripzeros: This will strip off the last field as long as it
            only contains '\x00's
        :param readAll: Don't use this! It's for internal use.
        :param nonumerics: Don't force fields after the first to numerics

        :return: The record as a tuple of fields
        :raises BBPyKeyNotFoundError: BBPyKeyNotFoundError if key is not found
        :raises BBPyPartialKeyFoundException: BBPyPartialKeyFoundException if
            only a partial key is found
        """
        if keynum is not None:
            self._setKeyNum(keynum)
        else:
            keynum = self.keynum

        if not self._f:
            raise MKEYEDReaderEOF("No Data file open")

        # If we have nothing to read then raise the EOF exception.
        if self._recordcount == 0:
            raise MKEYEDReaderEOF("File contains no records.")

        if key is not None:
            spec_key = key
        else:
            try:
                spec_key = self._cursor_spec.key
            except AttributeError:
                spec_key = None
        new_cursorspec = self.CursorSpec(
            spec_key, keynum, stripzeros, readAll, nonumerics)
        if self._cursor_spec != new_cursorspec:
            self._cursor = self.getIndex().cursor(key)
            self._cursor_spec = new_cursorspec

        try:
            found_key, found_addr = self._cursor.next()
        except StopIteration:
            found_key, found_addr = None, None
        self._currentkey = found_key

        if key is None or (found_key is not None and found_key == key):
            # If the key we found == the key we are searching for, we're good
            data = self._readMKEYEDRecord(found_addr)

            # split our data into fields
            if readAll:
                return ((found_key, found_addr),
                        self._splitRecordIntoFields(data, stripzeros))
            else:
                return self._splitRecordIntoFields(
                    data, stripzeros, nonumerics=nonumerics)

        elif found_key is not None and found_key.startswith(key):
            # If they are not equal but what we found starts with our search
            # key, then we have found a partial key
            # Reset cursor so next readRecord will start at next key
            last_spec = self._cursor_spec
            self._cursor_spec = self.CursorSpec(
                found_key, last_spec.keynum, last_spec.stripzeros,
                last_spec.readAll, last_spec.nonumerics)
            self._cursor = self.getIndex().cursor(key)

            raise BBPyPartialKeyFoundException(key, found_key)
        else:
            # Key doesn't match at all
            # Reset cursor to start of index.
            # This is the old mkeyed behaviour. It seems equally useful that
            # the next read would read the next record, mirroring the partial
            # key behaviour, but there may be callers that are expecting the
            # first record.
            self._cursor_spec, self._cursor = None, None

            message = "The requested key (%s) is not in the data file: %s."
            raise BBPyKeyNotFoundError(key, message % (key, self.filename))

    def open(self, f, mode="rb"):
        """Open an MKEYED datafile

        :param f: the full path to the datafile
        :param mode: The file open mode to open the file with. The default
            is "rb".
        """

        if hasattr(f, "read") and hasattr(f, "tell") and hasattr(f, "seek"):
            self._f = f
        else:
            self._f = open(str(f), mode)

        if hasattr(self._f, "name"):
            self.filename = self._f.name
        else:
            self.filename = "StringIO"

    def close(self):
        """\
        Close an open file handle and reset the state variables.
        """
        if self._f:
            self._f.close()

        self._setKeyNum(None)
        self._indexes = {}

    def next(self):
        """\
        Read the next record and advance the pointer

        This is part of support for the Python iteration protocol.
        """
        try:
            data = self.read()
            return data
        except (BBPyKeyNotFoundError, MKEYEDReaderEOF):
            # For iteration, StopIteration is the functional
            # equivalent of EOFError
            raise StopIteration

    def getStats(self):
        """Returns a tuple of the keysize, record count, and record size."""
        return (self.getKeylength(), self._recordcount, self._recordsize)

    def getKeylength(self):
        """\
        getKeyLength() returns the length of the key that the current instance
        of MKEYEDReader is looking at.  This is subject to change based on
        passing keynum to one of the read*/find methods. """

        if self._keysize:
            return self._keysize
        else:
            keysize = sum([x[1] for x in self.keys[self.keynum].key_segments])
            return keysize

    # Private methods

    def _checkFileType(self):
        """Throw an exception if this is an unsupported file type"""
        if FT_MKEYED != self._type or FT_MKEYED4GB != self._type:
            raise BBPyWrongFileTypeError(
                "MKEYEDReader cannot read this file type.")

    ALL_CONSTANTS = {
        FT_MKEYED: {
            'header_start': 0x0f,  # Offset of header section
            'header_size': 0x20,  # Size in bytes of header
            'header_layout': "!LLLLLLLL",  # Layout of header
            'addr_size': 0x4,  # Size of addresses in bytes
            'addr_layout': '!L',  # Layout of an address
            'keydef_start': 0x75,  # Offset of key definitions
            'record_offset': 0,  # Data offset within record
        },
        FT_MKEYED4GB: {
            'header_start': 0x19a,  # Offset of header section
            'header_size': 0x38,  # Size in bytes of header
            'header_layout': "!LQQQLQQQ",  # Layout of header
            'addr_size': 0x8,  # Size of addresses in bytes
            'addr_layout': '!Q',  # Layout of an address
            'keydef_start': 0x19,  # Offset of key definitions
            'record_offset': 4,  # Data offset within record
        }
    }

    def _readFileHeader(self):
        """Get file information from the pre-data header."""
        # From PRO/5 User's Guide, Chapter 1: Fundamentals, I/O
        # Concepts, Distinguishing Files From Devices
        # and FID() documentation
        #
        # [in bytes]
        # Position Size Description
        #        0    7 "<<bbx>>"
        #        7    1 File type
        #        8    1 Logical key size
        #        9    4 Number of records
        #       13    2 Bytes per record

        f = self._f
        f.seek(0)

        # Check the header
        idstring = f.read(7)

        # Is this a BBx data file?
        # The first 7 bytes must be "<<bbx>>"
        if "<<bbx>>" != idstring:
            self._type = FT_STRING  # STRING filetype
        else:
            data = f.read(8)

            try:
                # file type, key size, record count, record size
                # for MKEYED files, key size and record count are zero
                ft, ks, rc, rs = struct.unpack("!BBLH", data)
                if ft > 0 and ft < 8 or ft == 102:
                    self._type = ft
                else:
                    self._type = FT_STRING
                self._keysize = ks
                self._recordcount = rc
                self._recordsize = rs
                self._constants = self.ALL_CONSTANTS.get(
                    self._type, {})
            except:
                self._type = FT_STRING
                self._keysize = 0
                self._recordcount = -1
                self._recordsize = -1

            self._readMKEYEDHeader()
            self._readMKEYEDKeyDefinition()
            self._setKeyNum(0)

    def _readMKEYEDHeader(self):
        """Read MKEYED file information"""
        # From FIN() documentation, starting at hex dumps
        # Pos is hex offset, S is size in bytes
        # -4GB- -2GB-
        # Pos S Pos S Description
        # 19A 4  0f 4 Number of keys in this file
        # 19E 8  13 4 ? Address of first record ?
        # 1A6 8  17 4 Address of next new record
        # 1AE 8  1b 4 Number of records?
        # 1B6 4  1f 4 ?
        # 1BA 8  23 4 ?
        # 1C2 8  27 4 ?
        # 1CA 8  2b 4 File length in bytes
        #
        # 1D2 8  2f 4 Address of start of first key index
        # 1DA 8  33 4 Address of start of second key index
        # ... 8  .. 4 Address of start of next key index

        f = self._f
        f.seek(self._constants['header_start'])
        data = f.read(self._constants['header_size'])
        header = struct.unpack(self._constants['header_layout'], data)

        self._keycount = header[0]
        self._nextaddr = header[2]
        # the normal header has recordcount of zero for MKEYED files
        self._recordcount = header[3]
        self._filelength = header[7]

        # index information
        self._indexblocks = []
        data = convIntFromString(f.read(self._constants['addr_size']))
        while data:
            self._indexblocks.append(data)
            data = convIntFromString(f.read(self._constants['addr_size']))
        return header, self._indexblocks

    def _readMKEYEDKeyDefinition(self):

        """Read MKEYED key definition data"""
        f = self._f
        keys = [None] * 48  # 48 element array of None
        f.seek(self._constants['keydef_start'])
        key_def_data = f.read(48 * 8)  # 48 eight byte definitions
        key_definitions = struct.unpack("!" + "8s" * 48, key_def_data)

        for data in key_definitions:
            key = MKEYEDKey(data)
            if not key:  # Found the terminator
                break
            # Prior key
            pk = keys[key.key_number]
            if pk:  # if it is a key
                pk.addKey(key)
                key = pk
            keys[key.key_number] = key

        # Remove all the Nones
        keys = filter(None, keys)
        self.keys = keys

    def _readMKEYEDRecord(self, address):
        """Read a record from an MKEYED file based on address alone.

        TODO: It appears 4GB records have a 4-bytes '0xFE' prefix.
        This might be part of the 4GB format, or it signals a
        checksummed record.
        """
        if address:
            self._f.seek(address + self._constants['record_offset'])
        else:
            raise BBPyKeyNotFoundError
        return self._f.read(self._recordsize)

    def _setKeyNum(self, keynum):
        """Set the current keynum and clear cursor parameters."""
        if keynum != self.keynum:
            self.keynum = keynum
            self._currentkey = None
            self._cursor_spec = None
            self._cursor = None

    def getIndex(self):
        """Get the index for the current keynum."""
        keynum = self.keynum
        if keynum not in self._indexes:
            self._indexes[keynum] = MKEYEDIndex(
                keynum, self._f, self.getKeylength(),
                self._indexblocks[keynum], self._constants['addr_size'])
        return self._indexes[keynum]

    def _splitRecordIntoFields(self, data, stripzeros=False, nonumerics=False):
        """Split a MKEYED record into the delimited fields
        :param data: Data to read
        :param stripzeros: Strip the zeros off the end
        :param nonumerics: Don't force fields to numerics"""

        result = []
        fields = data.split("\x0a")
        # Try to convert the fields to numerics
        # NOTE: we may not want to convert our fields to numerics
        # automagically.  For now we'll try to convert all except the
        # first one.  The first one, containing a key, should never be
        # a numeric but those after it could be and since it is the
        # historic behavior, we'll leave it for now.
        # We now have a nonumerics for all fields in case we don't
        # want the conversion at all
        result.append(fields[0])
        for x in fields[1:]:
            if nonumerics:
                result.append(x)
            else:
                try:
                    f = float(x)
                except ValueError:
                    f = str(x)
                # Yes, this will append the post-terminator zeros as a
                # string.  There is no way for the Reader to know if
                # this is valid data or not.  The application needs to
                # handle it.
                result.append(f)

        if stripzeros:
            tmp = map(lambda x: x == '\x00', result[-1])
            if tmp and reduce(lambda x, y: x and y, tmp):
                result = result[:-1]

        result = tuple(result)

        if not result:
            result = ('', ())

        return result  # This is read-only


class MKEYEDIndex(object):
    """
    Represent an MKEYED Index

    An index maps keys to records. The index keys are ordered and stored in a
    tree structure using index blocks. Finding a particular key often requires
    reading several branch blocks to get to a leaf block.

    An MKEYED database may contain several indexes. The first will contain
    unique keys, but the additional indexes may have duplicates.
    """

    def __init__(
            self, keynum, mkeyed_file, keylength, root_address, pointer_size):
        """Initialize a L{MKEYEDIndex} instance.

        :param keynum: The number of this key index
        :param mkeyed_file: An open MKEYED file.
        :param keylength: The length of keys in this index.
        :param root_address: The address of the root index block.
        :param ptr_size: The size of address pointers in this MKEYED file.
        """
        self.keynum = keynum
        self.mkeyed_file = mkeyed_file
        self.keylength = keylength
        self.root_address = root_address
        self.pointer_size = pointer_size
        self.blocks = {}

    def get_block(self, block_address=None):
        """Get the L{MKEYEDIndexBlock} at a given address.

        :param block_address: The block address, or None for the root block
        :return an L{MKEYEDIndexBlock} instance
        """
        address = block_address or self.root_address
        if address not in self.blocks:
            self.blocks[address] = MKEYEDIndexBlock(
                self.mkeyed_file, self.keylength, address, self.pointer_size)
        return self.blocks[address]

    EdgeResult = namedtuple(
        'EdgeResult', ['positions', 'key', 'record_ptr', 'index_ptr'])

    def first(self):
        """Return the first entry in the index."""
        block = self.get_block()
        result = block.first()
        positions = [0]
        while result.index_ptr:
            positions.append(0)
            block = self.get_block(result.index_ptr)
            result = block.first()
        log("Returning first key {0!r}", result.key)
        return self.EdgeResult(tuple(positions), *result)

    FindResult = namedtuple(
        'FindResult',
        ['positions', 'record_ptr', 'prev_key', 'next_key', 'prev_index',
         'next_index'])

    def find(self, searchkey):
        """Find the first instance or insertion point for a key.

        If the key is an exact match, a result with a record address will be
        returned.  Otherwise, the result is the position where this key would
        appear if inserted. Partial keys will always have 'insert' returns.

        :param key: A full or partial key.
        :return: A L{MKEYEDIndex.FindResult}.
        """
        assert searchkey is not None,\
            "Key must be set. Use .first() to get first key."
        block = self.get_block()
        log("Looking for {0!r} in index {1}", searchkey, self.keynum)
        result = block.find(searchkey)
        positions = [result.pos]
        while (not result.record_ptr) and (result.next_index):
            log("Branching to {0:0{1}X}",
                result.next_index, self.pointer_size * 2)
            block = self.get_block(result.next_index)
            result = block.find(searchkey)
            positions.append(result.pos)
        return self.FindResult(tuple(positions), *result[1:])

    def cursor(self, searchkey=None):
        """Return (key, record_ptr) pairs starting at searchkey

        :param searchkey: A full key, partial key, or None
        :return the first key, record_ptr pair after the searchkey
        """
        if searchkey is None:
            result = self.first()
        else:
            result = self.find(searchkey)
        positions = result.positions
        block_tree = []
        block = self.get_block()
        for position in positions:
            block_tree.append(block.iterator(position))
            next_index = block.index_ptrs[position]
            if next_index:
                block = self.get_block(next_index)

        while block_tree:
            try:
                item = block_tree[-1].next()
            except StopIteration:
                block_tree.pop()
            else:
                if isinstance(item, MKEYEDIndexBlock.KeyResult):
                    yield item
                else:
                    assert isinstance(item, MKEYEDIndexBlock.IndexResult)
                    block = self.get_block(item.index_ptr)
                    block_tree.append(block.iterator())


class MKEYEDIndexBlock(object):
    """
    Represents an MKEYED Index Block

    An index block is a section in an MKEYED file that includes:
    - The index record count (1 Byte)
    - The address to the previous index (pointer size, 4 or 8 bytes)
    - The index records:
      - The index key (length varies by index)
      - The record address (pointer size, 4 or 8 bytes)
      - The address of the next index (pointer size, 4 or 8 bytes)

    This represents a section of the index tree.  The index keys are
    in order from least to greatest (A to Z), and the index addresses
    allow decending to more detailed portions of the tree.  If the key is
    in the index, then the value address gives the location of the
    full record.  If the key is not in the index, then:
    - If it is less than the first index key, use the first index address
      to descend the tree.
    - If it is between two index keys, use the index address between
      the the two keys.
    - If it after the last index key, use the last index address.

    If the index address is null, then you have decended to a leaf
    node, and the key is not in the MKEYED file.

    If many keys in the same file are searched, then the top index
    block may be scanned many times.
    """

    def __init__(self, mkeyed_file, keylength, start, ptr_size):
        """Read the index block at this location."""
        self.start = start
        layout1, layout2 = {
            4: ('!BL', '!LL'),
            8: ('!BQ', '!QQ'),
        }[ptr_size]
        mkeyed_file.seek(start)

        raw_data = mkeyed_file.read(1 + ptr_size)
        assert len(raw_data) == (1 + ptr_size), len(raw_data)
        record_count, prev_index = unpack(layout1, raw_data)
        record_size = keylength + (ptr_size * 2)
        self.index_size = 1 + ptr_size + (record_count * record_size)
        self.index_ptrs = [prev_index]

        self.keys = []
        self.record_ptrs = []
        raw_data = mkeyed_file.read(record_size * record_count)
        assert len(raw_data) == (record_size * record_count)
        for i in xrange(record_count):
            start = i * record_size
            key_end = start + keylength
            ptr_end = key_end + (ptr_size * 2)
            key = raw_data[start:key_end]
            record_ptr, next_index = unpack(layout2, raw_data[key_end:ptr_end])
            self.keys.append(key)
            self.record_ptrs.append(record_ptr)
            self.index_ptrs.append(next_index)

    FindResult = namedtuple(
        'FindResult',
        ['pos', 'record_ptr', 'prev_key', 'next_key', 'prev_index',
         'next_index'])

    def find(self, key, addressexclusions=None):
        """
        Get the related data for a given target key.

        Return is a 6-element namedtuple:
        - pos - If the key is in the index, the position in the index.
          If the key is not in the index, the "insertion" point, where
          the key would appear if added.
        - record_ptr - If the key is in the index, the address of the full
          record.  If the key is not in the index, then None
        - prev_key - The key in index proceeding the key, or None if
          no previous key in the index
        - next_key - The key in the index after the key, or None if
          no next key in the index
        - prev_ptr - The pointer to the index block with keys greater
          than prev_key and less than the target key, or null if at a
          leaf index block
        - next_ptr - The pointer to the index block with keys greater
          than the target key and less than the next_key, or null if
          at a leaf index block

        To find a record:
        1. Load the root index
        2. Call index.find:
           - If record_ptr is not None, you found it.
           - If prev_ptr and next_ptr are None, the key is not in the
             file.  If prev_key or next_key is None, your key is the
             first or last in the file.
           - If next_ptr is not None, load that index and go to 2.

        TODO: addressexclusions is due to iterating by keys rather
        than by index entries.  Remove when iterator is used instead.
        """
        assert key is not None, 'Key must be a real key'
        record_ptr = None
        prev_key = None
        next_key = None
        prev_index = None
        next_index = None

        pos = bisect_left(self.keys, key)
        try:
            found_key = self.keys[pos]
        except IndexError:
            found_key = None
        else:
            if addressexclusions:
                while self.record_ptrs[pos] in addressexclusions:
                    pos += 1
                    try:
                        found_key = self.keys[pos]
                    except IndexError:
                        found_key = None

        if found_key is not None and key == found_key:
            # The key is in this index
            record_ptr = self.record_ptrs[pos]
            if pos:
                prev_key = self.keys[pos - 1]
            try:
                next_key = self.keys[pos + 1]
            except IndexError:
                pass
            prev_index, next_index = self.index_ptrs[pos:pos + 2]
        elif pos == 0:
            # The key is before all keys in this index
            next_key = self.keys[0]
            prev_index = next_index = self.index_ptrs[0]
        elif found_key is None:
            # The key is after all keys in this index
            prev_key = self.keys[-1]
            prev_index = next_index = self.index_ptrs[-1]
        else:
            prev_key = self.keys[pos - 1]
            next_key = self.keys[pos]
            prev_index, next_index = self.index_ptrs[pos - 1:pos + 1]
        return self.FindResult._make(
            (pos, record_ptr, prev_key, next_key, prev_index, next_index))

    EdgeResult = namedtuple(
        'EdgeResult', ['key', 'record_ptr', 'index_ptr'])

    def first(self, start=0):
        """
        Get the first key, record pointer, and previous index pointer.

        The return is a namedtuple:
        - key - The first key in the index
        - record_ptr - The pointer to the first record
        - index_ptr - The pointer to the index of keys before the
          first key

        Once you've found a target key and the next key in the index,
        you can find the next key in the data file:
        1. If next_ptr is None, then the next_key is the next key
        2. Load the index for next_ptr
        3. Call index.first, setting next_key to key and next_ptr to
        index_ptr.
        4. Return to step 1

        You can use a similar process to find the first key in the
        file.

        Duplicate keys can be created when a tree rebalance fails for
        some reason. In these cases, the caller may need to start
        somewhere other than the first entry in the index block.
        """
        if start < 0:
            raise IndexError(start)
        key = self.keys[start]
        record_ptr = self.record_ptrs[start]
        index_ptr = self.index_ptrs[start]
        return self.EdgeResult._make((key, record_ptr, index_ptr))

    KeyResult = namedtuple('KeyResult', ['key', 'record_ptr'])
    IndexResult = namedtuple('IndexResult', ['index_ptr'])

    def iterator(self, start=None):
        """Return an iterator over the index block.

        :param start: Start with key at this position.  If omitted or None,
            start with the previous index.
        :return An iterator over the index block
        """
        pos = start or 0
        if start is None and self.index_ptrs[0]:
            yield self.IndexResult(self.index_ptrs[0])
        while True:
            try:
                yield self.KeyResult(self.keys[pos], self.record_ptrs[pos])
                index_ptr = self.index_ptrs[pos + 1]
                if index_ptr:
                    yield self.IndexResult(index_ptr)
            except IndexError:
                return
            else:
                pos += 1


class MKEYEDWriter(object):
    """Builds a batch of write requests and passes to SH.BBX.WRITE"""

    def __init__(self, configpath=""):
        """
        :param configpath: Allows the programmer to specify a path to
            place in front of the config file (bbw.config).

        :return: Instance of a L{MKEYEDWriter}.
        """

        self.clear()
        if configpath and configpath[-1] != "/":
            configpath += "/"
        self.configpath = configpath

    def clear(self):
        """ Reset this instance, clear any queued write requests. """
        self.batch = []

    def delete(self, file, key):
        """ Add a delete request to the batch. """
        self.batch.append(
            {"filename": str(file), "key": str(key), "record": "",
             "numcount": "0"})

    def write(self, file, key, rec, nums=None, checkrec=True):
        """ Add a write request to the batch.

        :param file: The basename of a BBx data file.
          (i.e. "ELFSUS")
        :param key: key of the record to be written.
        :param rec: record to be written (as a BBPyString)
        :param nums: list or tuple of numbers to be written as numerics
        :param checkrec: a failsafe measure to check your keys against your
            record

        """

        # We have to scrub the data really well before we pass it to BBx
        if type(rec) == strings.BBPyString:
            rec = str(rec)
        if (
            not isinstance(rec, basestring) or
            not isinstance(key, basestring) or
            not isinstance(file, basestring)
        ):
            raise BBPyWriterTypeError(
                "MKEYEDWriter can only write strings")
        if file.find('/') != -1:
            raise BBPyWriterTypeError(
                "Pass only the filename, BBx will figure its own context.")
        if checkrec and not rec.startswith(key):
            raise BBPyWriterUnknownError(
                "Your record string does not include the key you passed."
                " {}:{}".format(key, rec))

        key = str(key)
        file = str(file)
        # OK, now we can add it to the queue.
        if not nums:
            self.batch.append(
                {"filename": file, "key": key, "record": rec, "numcount": "0"})
        else:
            self.batch.append(
                {"filename": file, "key": key, "record": rec,
                 "numerics": str(nums), "numcount": str(len(nums))})

    def flush(self):
        """ Send the batched write requests to the BBx slave routine. """

        # add a path if we have one
        config = self.configpath + PRO5CONFIG

        if self.batch != []:

            # grab the max numeric size, BBx needs this to not waste memory
            maxnumerics = reduce(lambda x, y: x > y and x or y,
                                 map(lambda x: int(x['numcount']), self.batch))
            outbuff = (len(self.batch), maxnumerics) + (self.batch,)
            cmd = "%s -q -c%s -tIO %s" % (PRO5, config, 'SH.BBX.WRITE')
            p = Popen([cmd], shell=True, stdin=PIPE, stdout=PIPE)
            p.stdin.write(outbuff.__str__() + '\x00')
            p.stdin.close()
            output = p.stdout.read()
            p.stdout.close()
            try:
                resp = eval(output)
            except:
                resp = 'Failed on evaluating: "%s"' % output
            if resp.find("SUCCESS!") == -1:
                raise BBPyWriterIOError(resp)
            self.clear()

    def __del__(self):
        """ Called to clean up this object when it gets deleted. """
        self.flush()


class MKEYEDKey(object):
    """A key for an MKEYED data file"""
    # [in bytes]
    # Position Size Description
    #        1    1 Key number
    #        2    1 Field in record
    #        3    2 Offset in field/record (0 based, 1024 max. value)
    #        5    1 Segment length
    #        6    1 Modifier flags
    #        7    2 zeros

    field_number = None
    key_number = None
    key_segments = None
    mod_flags = None
    segment_length = None
    segment_offset = None

    def __init__(self, data):
        """Create a key"""
        self.parseData(data)

    def parseData(self, data):
        """Parse the key definition data"""
        kn, fn, o, l, m, z = struct.unpack("!BBHBBH", data)
        if 255 == kn:  # This is a key definition terminator
            return
        self.key_number = kn
        self.field_number = fn
        self.segment_offset = o
        self.segment_length = l
        self.key_segments = [(o, l)]
        self.mod_flags = m
        assert 0 == z, "Zeros in key definition != 0"

    def addKey(self, key):
        """Update key segments from an additional key definition"""
        self.key_segments.append((key.segment_offset,
                                  key.segment_length))

    def __len__(self):
        if self.key_segments:
            # Note that the zip(*arg) format consumes the outer
            # sequence and that zip() is its own inverse:
            #
            #   >>> a = [(1, 2), (3, 4)]
            #   >>> a == zip(*zip(*a))
            #   True
            #
            # Explained about half-way down this page:
            # http://docs.python.org/ref/calls.html
            # and again near the bottom of this e-mail:
            # http://mail.python.org/pipermail/python-list/2003-April/199780.html
            return sum(zip(*self.key_segments)[1])
        else:
            return 0

    def __nonzero__(self):
        """Boolean evaluation of the object

        If the key definition is complete and the key number is a
        whole number less than 16, then the object is True.
        """
        return self.key_number is not None and (-1 < self.key_number < 16)


class BBPyKeyNotFoundError(Exception):
    """\
    Raised when a specified key is not found in the data file.

    :ivar searchkey: The key being searched for.
    :ivar recentkey: The key found just before the searchkey's absence
        was detected
    :ivar recordaddr: The file offset of recentkey.
    :ivar message: Message supplied by the module about the specific area.
        where the key was not found
    """

    DEFAULT_MESSAGE = "The requested key (%s) is not in the data file: %s."

    def __init__(
            self, searchkey=None, recentkey=None, recordaddr=None,
            message=DEFAULT_MESSAGE):
        """Constructor for a BBPyKeyNotFoundError."""
        self.args = (searchkey, recentkey, recordaddr, message)
        self.searchkey = searchkey
        self.recentkey = recentkey
        self.recordaddr = recordaddr
        self._message = message

    def message(self):
        """This is totally to accommodate Python 2.6's deprecation of
        the 'message' attributes of BaseException.
        http://bugs.python.org/issue6844 covers the fix for this but I
        suspect that the, ahem *slow* nature of our upgrade process
        means that it will be awhile before we hit it. In the meantime
        I'd prefer not to have spurious Deprecation messages."""
        return self._message
    message = property(message)


class BBPyPartialKeyFoundException(Exception):
    """\
    Raised when a full key is not found in the data file, but a partial key
    exists.

    :ivar searchkey: The key being searched for.
    :ivar recordkey: The first partial key match.
    """
    def __init__(self, searchkey, recordkey):
        """Constructor for a BBPyPartialKeyFoundException."""
        self.args = (searchkey, recordkey)
        self.searchkey = searchkey
        self.recordkey = recordkey


class BBPyWrongFileTypeError(Exception):
    """Raised if the data file is not a type MKEYEDReader can read"""


class MKEYEDReaderEOF(Exception):
    """Used as a flag in the event the reader reaches the End Of File (EOF)"""


class BBPyWriterTypeError(Exception):
    """Raised when the programmer tries to pass a dict instead of a string."""


class BBPyWriterIOError(Exception):
    """Raised when the writer cannot communicate with the server."""


class BBPyWriterUnknownError(Exception):
    """Raised whenever the server returns and error code"""

# vi: set tabstop=4 expandtab textwidth=80 filetype=python:
