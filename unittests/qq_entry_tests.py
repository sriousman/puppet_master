"""All integration testing for Quick Quote rater"""
from robot.api import logger
import unittest
from selenium.webdriver.firefox.options import Options
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestVehicle(unittest.TestCase):
    """ 
Run a host of tests on the Vehicle Section in qq.entry
    """

    # def __init__(self, vdev):
    #     self.vdev = vdev
        
    #     options = Options()
    #     options.add_argument("--devtools --headless")
        
        # start docker containers
        # get esiredCapabilities dcap = DesiredCapabilities.chrome();
        # String driverPath = System.getProperty("user.dir") + "/exe/chromedriver";
        # System.setProperty("webdriver.chrome.driver", driverPath);

        # // You should check the Port No here.
        # URL gamelan = new URL("http://localhost:32771/wd/hub");
        # WebDriver driver = new RemoteWebDriver(gamelan, dcap);





    def setUp(self):


        self.driver = webdriver.Remote(
            command_executor = 'http://127.0.0.1:4444/wd/hub',
            desired_capabilities= DesiredCapabilities.CHROME)

        self.driver.implicitly_wait(10)



    def test_title(self):
        self.driver.get('http://www.google.com')
        
        self.assertIn('Google', self.driver.title)

    def tearDown(self):
        self.driver.close()
    # def reset_page(self, driver, url):
    #     """
    #     Resets the page to perform another action
    #     """
        # driver.get(url)??
    
    # def test_vin(self):
    #     """Entering a VIN and a year should pull vehicle info"""
        #setup opens new page in (thought: use with to manage context)
        #enter vin
        #enter year
        #wait for load
        #get 
    


## Use mock to build input libraries?
## log screenshots during driver execution using .save_screenshot("filename.png")
## use the robot logger to put it in a nice html


"""




Start a new business quote
Enter a VIN number
Enter the VIN year

 "Year" should be correct

 "Make" should be correct

 "Model" should be correct

 "Year" input field should be disabled

 "Make" dropdown should be disabled

 "Model" dropdown should be disabled


Entering a year should pull makes


Start a new business quote
Input the year
Click the "Make" dropdown

 "Make" dropdown is populated with makes


Selecting a year and make should pull models 


Start a new business quote
Input the year
Select vehicle make
Click the "Model" dropdown

 "Model" dropdown is populated with models"""


suite = unittest.TestLoader().loadTestsFromTestCase(TestVehicle)
unittest.TextTestRunner(verbosity=2).run(suite)
