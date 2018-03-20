'''Handles identifying policies available for rewrite'''

from bbpy.strings import BBPyString
from bbpy.files.template import getTpl
from eicpy.insureds import policelink


class Policy(object):
    '''Rewrite policy finder'''

    template = getTpl(['AGPPI.TPL'])

    def __init__(self, record_string):
        '''Handle policies

        Args:
            record_string (str): Record string from AGPPI
        '''
        self.record = BBPyString(record_string, self.template)
        self.policy_number = self.record.pol.strip()
        self.get_billing()

    def get_billing(self):
        '''Retrieve the billing status for the policy'''
        pepolicy = policelink.Policy(self.policy_number, self.record.exp)
        pepolicy.get_billingstatus()
        self.billing = pepolicy.billing

    def is_rewritable(self):
        '''Determine if policy is eligible to be rewritten

        Returns:
            True or False rewrite state
        '''
        if self.record['trg'] != 'C':
            return False

        if self.billing['accept'] == 'T':
            return True

        return False

    def is_renewable(self):
        '''Determine if policy is eligible to be renewed

        Returns:
            True or False renewal state
        '''
        if self.record['trg'] != 'T':
            return False

        if self.billing['accept'] in ('R', 'D'):
            return True

        return False

    def is_endorsable(self):
        '''Determine if policy is eligible to be endorsed

        Returns:
            True or False endorsement state
        '''
        if self.record['trg'] == 'B':
            return True

        return False
