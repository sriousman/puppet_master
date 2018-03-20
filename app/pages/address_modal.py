from base import BasePage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
from locators.address_modal_locs import AddressModalLocators as aml


class AddressModal(BasePage):
    """
    A class for the address modal popup action methods
    """

    #BUTTON CLICKS
    def click_different_street_address_option_yes(self):        
        element = self.driver.find_element(
            *aml.DIFF_ADDRESS_RADIO_YES)
        element.click()

    def click_different_street_address_option_no(self):
        element = self.driver.find_element(
            *aml.DIFF_ADDRESS_RADIO_NO
        )
        element.click()

    def click_address_save_button(self):        
        element = self.driver.find_element(
            *aml.SAVE_BUTTON)
        element.click()

    def click_address_cancel_button(self):        
        element = self.driver.find_element(
            *aml.CANCEL_BUTTON)
        element.click()


    