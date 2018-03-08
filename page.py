from element import BasePageElement
from locators import QQRewriteARLocators

class AddressTextElement(BasePageElement):
    """
    This class gets the search text from the specified locator
    """

    #The locator for search box where search string is entered
    locator = 'q'


class BasePage(object):
    """
    Base class to initialize the base page 
    that will be called from all pages
    """

    def __init__(self, driver):
        self.driver = driver


class QQRewriteAutoRaterPage(BasePage):
    """
    A class for Quick Quote Auto Rater page action methods
    """
    #VERIFIERS
    def is_title_matches(self):
        """Verifies that title is what it should be"""
        return "Quick Quote Auto Rater" in self.driver.title

    #INPUTS

    #BUTTON CLICKS
    def click_address_button(self):        
        element = self.driver.find_element(
            *QQRewriteARLocators.ADDRESS_BUTTON)
        element.click()

    def click_address_save_button(self):        
        element = self.driver.find_element(
            *QQRewriteARLocators.SAVE_BUTTON)
        element.click()

    def click_address_cancel_button(self):        
        element = self.driver.find_element(
            *QQRewriteARLocators.CANCEL_BUTTON)
        element.click()
    




class SearchResultsPage(BasePage):
    """
    Search results page action methods come here
    """

    def is_results_found(self):
       
        return "No results found." not in self.driver.page_source