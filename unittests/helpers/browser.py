from selenium import webdriver
from selenium selenium.logging import LogEntrie
from selenium.webdriver.common.keys import Keys

from robot.api import logger

import os


# Might use this for automating page profiling and scaffolding
class Browser(object):
    """Handles web browser
    
    attributes:
    location - The location of the browser/docker container
    """
    def __init(self, location):
        """Class Initialization Function"""

    def __call__(self):
        """Class call"""
    
    def startDriver(self,browser="chrome"):
        """Starts the driver"""
        #Make sure that the browser parameter is a string
        assert isinstance(browser,str)

        #Standardize the browser selection string
        browser = browser.lower().strip()
        #Start the browser
        if browser=="chrome":
            self.driver = webdriver.Chrome(self.location,  )

    def closeDriver(self):
        """Close the browser object"""
        #Try to close the browser
        try:
            self.driver.close()
            
        except Exception as e:
            print("Error closing the web browser: {}".format(e))

    def getURL(self,url):
        """Retrieve the data from a url"""
        #Retrieve the data from the specified url
        data = self.driver.get(url)

        return data

    def __enter__(self):
        """Set things up"""
        #Start the web driver
        self.startDriver()
        return self

    def __exit__(self, type, value, traceback):
        """Tear things down"""
        #Close the webdriver
        self.closeDriver()

    def setup_logger(self):
        

#element.clear()
#element.sendKeys()






if __name__ == '__main__':
    url = 'http://www.python.org'
    with Browser() as browser:
        print(browser.getURL(url))




        # try starting with options --dump-dom 
        #                           --print-to-pdf
        #                           --enable-logging
    