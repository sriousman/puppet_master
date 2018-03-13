from base import BasePage
from locators.qq_entry_locs import QQEntryLocators as qqe
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys


class QQEntryPage(BasePage):
    """
    A class for Quick Quote Auto Rater page action methods
    """

    def click_rate_button(self):        
        element = self.driver.find_element(*qqe.RATE_BUTTON)
        element.click()
    
    def click_save_button(self):
        element = self.driver.find_element(*qqe.SAVE_BUTTON)
        element.click()

    def click_address_cancel_button(self):        
        element = self.driver.find_element(*qqe.CANCEL_BUTTON)
        element.click()

