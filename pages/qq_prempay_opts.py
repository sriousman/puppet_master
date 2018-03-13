"""Quick Quote Premium Payment Options"""
from base import BasePage
from locators.qq_prempay_locs import QQPremPayLocators as qqp
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys


class QQPremPayPage(BasePage):

    def click_application_button(self):
        element = self.driver.find_element(
            *qqp.APPLICATION_BUTTON
        )
        element.click()
