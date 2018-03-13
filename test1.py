from pages.qrw_autorater import QRWAutoRaterPage as qrw
from pages.address_modal import AddressModal as am
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import unittest


# class DriverDeletionTest(unittest.TestCase):
#     """Tests the deletion of drivers on a rewrite with at least 2 drivers"""

#     def setUp(self):
#         USRS = ['5121','4444','5331']
#         Policies = ["N35038863", "N24033985", "N03522676"]
#         PASSWORD = 'test'
#         environ = "@cherry-pick-4a874f92.dev.equityins.net/cgi-bin/bbw.sh?pgm=POLICY&policyno="
#         options = Options()
#         options.add_argument("--devtools")
#         self.driver = webdriver.Firefox(firefox_options=options)
#         self.driver.implicitly_wait(10)
#         self.urls = ['http://'+u[0]+':'+PASSWORD+environ+u[1] for u in zip(USRS,Policies)]

#     def test_delete_popup_open(self):
#         """
#         Tests the delete driver popup window to make sure that it
#         is opening properly.
#         """
#         pass

#     def test_delete_popup_close(self):
#         """
#         Tests the delete driver popup window to make sure that it
#         is closing properly.
#         """
#         pass
    
#     def test_named_driver_exclusion_text(self):
#         """
#         Tests the delete driver popup window to make sure that it
#         is showing the proper text when 'yes' radio button is 
#         selected for the 'Is the driver still a member of the
#         household?' question in the popup.
#         """
#         pass

#     def test_non_household_driver_removed(self):
#         """
#         Tests that a driver is in fact deleted when 'no' radio
#         button is selected.
#         """
#         pass

#     def test_household_driver_removed(self):
#         """
#         Tests that a driver is in fact deleted when 'yes' radio
#         button for household driver is selected.
#         """
#         pass

#     def test_named_driver_removal_invalid_popup(self):
#         """
#         Tests alert message when attempting to delete the
#         named driver on the policy.
#         """
#         pass


class TestAddressModal(unittest.TestCase):
    """
    Contains tests for the Address Modal in QQ Rewrite Auto Rater
    """
    def setUp(self):
        self.url = "http://5121:test@master.dev.equityins.net/cgi-bin/qrw.entry.py?mode=rewrite&key=N35062747&agent=5121&expdate=071318"
        options = Options()
        options.add_argument("--devtools")
        self.driver = webdriver.Firefox(firefox_options=options)
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)

    def test_popup_shows(self):
        """The "Edit Address" popup should show"""
        qrw_entry_page = qrw(self.driver, self.url)
        qrw_entry_page.click_address_button()
        assert("Quick" in self.driver.title)

    # def test_popup_closes(self):
    #     """The "Edit Address" popup should close""" 
    #     pass

    # def test_mailing_address_change(self):
    #     """Previously entered values should appear in the "Mailing Address" fields """
    #     pass

    # def test_invalid_mailing_addresss_zip(self):
    #     """Invalid zip should show flash message"""
    #     pass

    # def test_mailing_address_zip(self):
    #     """Valid zip should show city and state values"""
    #     pass

    # def test_street_address_placeholder(self):
    #     """The Alternate street address form should show"""

    #     pass
    
    # def test_garaged_address_explanation_placeholder(self):
    #     """The "Please Explain" textarea should show"""

    #     pass

    # def test_address_modal_data_save(self):
    #     """New data entered should save properly"""
    #     pass

    def tearDown(self):
        self.driver.close()

suite = unittest.TestLoader().loadTestsFromTestCase(TestAddressModal)
unittest.TextTestRunner(verbosity=2).run(suite)
