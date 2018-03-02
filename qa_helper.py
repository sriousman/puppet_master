"""
Utility to assist QA Specialist in opening rewrites in
multiple browsers in multiple states.
Future: assist in finding suitable policies
Future: assist in copying policies to testing environments
Future: assist in opening browsers in VMs (IE and Edge)
Future: assist in keeping console error logs
Future: assist in keeping notes and writing test reviews
"""

from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time


class App(object):
    """
Author: Gregory Covington
Date: 03/02/2018
Description:
The QA Helper is a utility that uses Selenium Library to
assist the QA Specialist in testing accross a range of
different browsers and OSes, situations,and states.

Attritbutes:
    USRS        -   list of testing agents' numbers
    PASSWORD    -   the pass for the tesing agents


    """

    USRS = ['5121','4444','5331']
    PASSWORD = 'test'
    qa_specialist = 'Greg'

    def main_loop():
        """
    Manages the UI.
        """

    def get_policies():
        # states = ['ok','mo','ar']
        # policies = []
        # for s in states:
        #     try:
        #         p = input('Enter policy no. for {} rewrite'.format(s)).upper()
        #         if p.startswith('N'):
        #             policies.append(p)
        return ["N35023892", "N24051785", "N03576691"]


    def get_test_environment():
    """
        Prompts user for testing environment, verifies and
        @returns string
    """
        return  "@cherry-pick-4a874f92.dev.equityins.net/cgi-bin/bbw.sh?pgm=POLICY&policyno="


    def build_urls():
        pols = get_policies()
        environ = get_test_environment()
        return ['http://'+u[0]+':'+PASSWORD+environ+u[1] for u in zip(USRS,pols)]


    # def check_browser_errors(driver):
    #     """
    #     Checks browser for errors, returns a list of errors
    #     :param driver:
    #     :return:
    #     """
    #     try:
    #         browserlogs = driver.get_log('browser')
    #     except (ValueError, WebDriverException) as e:
    #         # Some browsers do not support getting logs
    #         LOGGER.debug("Could not get browser logs for driver %s due to exception: %s",
    #                      driver, e)
    #         return []

    #     errors = []
    #     for entry in browserlogs:
    #         if entry['level'] == 'SEVERE':
    #             errors.append(entry)
    #     return errors
    ## TODO
    #  find way to check for when browser is closed, driver is stopped and write errors to a file


    def puppet_master():
        """
    The master of puppets controls the browsers and hopefully
    in the future the Docker containers and the The World!!!
        """
        urls = build_urls()
        print(urls)
        # Open Firefox browsers in all 3 states and go to 
        # Quick Quote Rewrite Auto Rater Page
        for u in urls:
            options = Options()
            options.add_argument("--devtools")
            driver = webdriver.Firefox(firefox_options=options)
            driver.get(u)
            driver.find_element(By.XPATH, '//a[text()="Quote a rewrite with change"]').click()
        
        # Open Chrome browsers in all 3 states and go to 
        # Quick Quote Rewrite Auto Rater
        for u in urls:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(chrome_options=options)
            driver.get(u)
            driver.find_element(By.XPATH, '//a[text()="Quote a rewrite with change"]').click()


if __name__ == '__main__':
    main()
