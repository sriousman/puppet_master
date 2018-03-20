'''Handles identifying policies available for rewrite'''

from bbpy.files.mkeyed import MKEYEDReader
from policy import Policy
import utils


class Search(object):
    '''Rewrite policy finder'''

    keylength = 23
    datafile = '/eic/data/AGPPI'
    dbfw21_file = '/eic/data/DBFW21'

    def __init__(self):
        '''Initialize a policy search

        Returns:
            policies (list): List of policy numbers
        '''
        self.reader = MKEYEDReader(self.datafile)

    def find(self, keys, count, filter_by=lambda policy: True):
        '''Find records that meet requirements

        Args:
            keys (list): List of keys to use as starting keys
            count (int): Number of results to return
            filter_by: Filter criteria

        Returns
            A list of policies
        '''
        policies = []
        for key in keys:
            start_key = utils.get_starting_key(key, self.keylength, self.reader)

            for rec in self.reader.readGenerator(start_key):
                pol = Policy(rec)
                if filter_by(pol):
                    policies.append(pol.record.pol.strip())

                if len(policies) > count:
                    return policies
        return policies


    def find_rewrites(self, keys, count):
        '''Search for policies for rewrite based on triggers and billing status

        Args:
            keys (list): List of starter keys
            count (int): Number of results to return

        Returns:
            List of policies eligible for rewrite
        '''
        return self.find(
            keys,
            count,
            filter_by=lambda policy: policy.is_rewritable()
        )

    def find_renewals(self, keys, count):
        '''Search for policies for renewals based on triggers and billing status

        Args:
            keys (list): List of starter keys
            count (int): Number of results to return

        Returns:
            List of policies eligible for renewal
        '''
        return self.find(
            keys,
            count,
            filter_by=lambda policy: policy.is_renewable()
        )

    def find_endorsements(self, keys, count):
        '''Search for policies for endorsements based on triggers and billing status

        Args:
            keys (list): List of starter keys
            count (int): Number of results to return

        Returns:
            List of policies eligible for endorsing
        '''
        return self.find(
            keys,
            count,
            filter_by=lambda policy: policy.is_endorsable()
        )

    def find_rewritten(self):
        '''Search for policies that were rewritten the day before

        Returns:
            List of policies 
        '''
        reader = MKEYEDReader(self.dbfw21_file)
        policies = [
            record[26:35]
            for record in reader
            if record[20:21] == 'T'
        ]

        return policies

    @staticmethod
    def get_rewrites(state, count=10):
        '''Retrieve a list of policies eligible for rewrite

        Args:
            state (str): 2 char state abbreviation
            count (int): Number of results to return

        Returns:
            A list of policies
        '''
        keys = utils.get_keys(state)
        searcher = Search()
        rewrites = searcher.find_rewrites(keys, count)
        return rewrites

    @staticmethod
    def get_renewals(state, count=10):
        '''Retrieve a list of policies eligible for renewal

        Args:
            state (str): 2 char state abbreviation
            count (int): Number of results to return

        Returns:
            A list of policies
        '''
        keys = utils.get_keys(state)
        searcher = Search()
        renewals = searcher.find_renewals(keys, count)
        return renewals

    @staticmethod
    def get_endorsements(state, count=10):
        '''Retrieve a list of policies eligible for endorsing

        Args:
            state (str): 2 char state abbreviation
            count (int): Number of results to return

        Returns:
            A list of policies
        '''
        keys = utils.get_keys(state)
        searcher = Search()
        endorsements = searcher.find_endorsements(keys, count)
        return endorsements

    @staticmethod
    def get_rewritten():
        '''Retrieve a list of policies that were rewritten the day before

        Returns:
            A list of policies
        '''
        searcher = Search()
        return searcher.find_rewritten()
