'''Utilities for policy searches'''

from bbpy.files.mkeyed import BBPyPartialKeyFoundException

starting_keys = {
    'OK': '090N35',
    'AR': '090N03',
    'MO': '090N24'
}


def get_keys(state):
    '''Get starting keys from state if one was given

    Args:
        state (str): 2 char state

    Returns:
        A list of starting keys
    '''
    if state in starting_keys:
        return [starting_keys[state]]
    return starting_keys.values()


def get_starting_key(key, keylength, reader):
    '''Find the key for the first record that matches our key

    Args:
        reader (object): Reader for a BBx file
        key (str): Partial key to start the search

    Returns:
        Full key
    '''
    try:
        startrec = reader.read(key=key)
    except BBPyPartialKeyFoundException:
        startrec = reader.read()
    return startrec[:keylength]
