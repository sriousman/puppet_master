from base import BasePage
from locators.qrw_autorater_locs import QRWAutoRaterLocators as qrw
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys


class QRWAutoRaterPage(BasePage):
    """
    A class for Quick Quote Auto Rater page action methods
    """

    def click_rate_button(self):        
        element = self.driver.find_element(*qrw.RATE_BUTTON)
        element.click()
    
    def click_exit_button(self):
        element = self.driver.find_element( *qrw.EXIT_BUTTON)
        element.click()

    def click_address_button(self):        
        element = self.driver.find_element(*qrw.ADDRESS_BUTTON)
        element.click()