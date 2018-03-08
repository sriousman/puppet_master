from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import page
import unittest
import time

class DriverDeletionTest(unittest.TestCase):
    """Tests the deletion of drivers on a rewrite with at least 2 drivers"""

    def setUp(self):
        USRS = ['5121','4444','5331']
        Policies = ["N35038863", "N24033985", "N03522676"]
        PASSWORD = 'test'
        environ = "@cherry-pick-4a874f92.dev.equityins.net/cgi-bin/bbw.sh?pgm=POLICY&policyno="
        options = Options()
        options.add_argument("--devtools")
        self.driver = webdriver.Firefox(firefox_options=options)
        self.driver.implicitly_wait(10)
        self.urls = ['http://'+u[0]+':'+PASSWORD+environ+u[1] for u in zip(USRS,Policies)]

    def test_delete_popup_open(self):
        """
        Tests the delete driver popup window to make sure that it
        is opening properly.
        """
        pass

    def test_delete_popup_close(self):
        """
        Tests the delete driver popup window to make sure that it
        is closing properly.
        """
        pass
    
    def test_named_driver_exclusion_text(self):
        """
        Tests the delete driver popup window to make sure that it
        is showing the proper text when 'yes' radio button is 
        selected for the 'Is the driver still a member of the
        household?' question in the popup.
        """
        pass

    def test_non_household_driver_removed(self):
        """
        Tests that a driver is in fact deleted when 'no' radio
        button is selected.
        """
        pass

    def test_household_driver_removed(self):
        """
        Tests that a driver is in fact deleted when 'yes' radio
        button for household driver is selected.
        """
        pass

    def test_named_driver_removal_invalid_popup(self):
        """
        Tests alert message when attempting to delete the
        named driver on the policy.
        """
        pass


class AddressModalTest(unittest.TestCase):
    pass






def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") != None


def main():
    
    

    # for u in urls:
    driver.get(urls[0])
    
    driver.find_element(By.XPATH, '//a[text()="Quote a rewrite with change"]').click()
    
    row = driver.find_element(By.XPATH, '//tr[@id="drivers-row_1"]//*[@value="X"]')
    time.sleep(2)
    row.click()
        # row.find_element(By.XPATH, '//input[@value="X"]').click()
        # driver.quit()
    cancel = driver.find_element(By.XPATH, '//div[@class="ui-dialog-buttonset"]//*[text()="Cancel"]')
    time.sleep(2)
    cancel.click()

    row.click()

    household_yes = driver.find_element_by_id('household-member-yes')
    household_yes.click()

    cancel.click()

    row.click()

    household_no = driver.find_element(By.XPATH, '//input[@value="no"]')

    household_no.click()

    ok = driver.find_element(By.XPATH, '//div[@class="ui-dialog-buttonset"]//*[text()="OK"]')
    ok.click()

    Add_driver = driver.find_element_by_id('drAdd')
    Add_driver.click()
    Keys.TAB
    first_name = driver.find_element_by_xpath('//input[@id="firstname/OID(3)")]')
    first_name.send_keys('jon')



if __name__ == '__main__':
    main()

