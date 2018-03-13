from elements.base import BasePageElement

class BasePage(object):
    """
    Base class to initialize the base page 
    that will be called from all pages
    """

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    