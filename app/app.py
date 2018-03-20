from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import sys
import csv
import thread
import time
import traceback
import datetime as dt
import json


class App(object):
    """
Author: Gregory Covington
Date: 03/02/2018
Description:
The QA Helper is a utility that uses Selenium Library to
assist the QA Specialist in testing accross a range of
different browsers and OSes, situations,and states.

Attritbutes:
    PASSWORD    -   the pass for the tesing agents
    sfile       -   json file with saved data
    qa_specialis-   name of the current qa specialist
    data        -   dict of loaded json data
    USRS        -   list of test agents
    """


    def __init__(self):
        self.today = dt.datetime.now().strftime("%m/%d/%Y")
        self.USRS = ['5121','5331','4444']
        self.PASSWORD = 'test'
        self.sfile = './data.json'
        self.data = {}
        self.qa_specialist = 'Greg'
        
        # load saved data
        self.load_sfile()

    def load_sfile(self):
        with open(self.sfile, 'r') as f:
            self.data = json.load(f)
    
    def save_sfile(self):
        with open(self.sfile, 'w') as f:
            json.dump(self.data, f)

    def set_vdev(self):
        if self.data["vdev"]:
            print("The current vdev is set to {} ".format(self.data["vdev"]))
        else:
            print("No current vdev.")
        vdev = raw_input("Enter a vdev: ")
        if vdev != '':
            self.data["vdev"] = vdev

    def set_policies(self):
        choice = raw_input("Do you want to change (R)ewrites or (E)ndorsements?").strip().lower()
        if choice == 'r':
            ref = self.data["rewrites"]
            print("Policies flagged for rewrite:")

            for indx, pol in enumerate(ref, start=1):
                print("{}: {} - {} {}".format(indx, * pol.values()))

            try:
                change = raw_input("\nType the number to change a policy or hit enter to cont...\n")
            except Exception as e:
                print(e)
                print("Enter a number")
            else:
                if change:
                    new_pol = raw_input("enter a new policy number: ")
                    save = raw_input("Are you sure you want to change {}, to {}".format(ref[int(change)-1]["policy"], new_pol))
                    if save == 'y':
                        ref[int(change) - 1]["policy"] = new_pol
                    else:
                        print("nothing saved!")
                        time.sleep(1)

        elif choice = 'e':
            ref = self.data["endorsements"]
            print("\nPolicies flagged for endorsements:")

            for indx, pol in enumerate(ref, start=1):
                print("{}: {} - {} {}".format(indx, * pol.values()))
            try:
                change = raw_input("\nType the number to change a policy or hit enter to cont...\n")
            except Exception as e:
                print(e)
                print("Enter a number")
            else:
                if change:
                    new_pol = raw_input("enter a new policy number: ")
                    save = raw_input("Are you sure you want to change {}, to {}".format(ref[int(change)-1]["policy"], new_pol))
                    if save == 'y':
                        ref[int(change) - 1]["policy"] = new_pol
                    else:
                        print("nothing saved!")
                        time.sleep(1)

        
    def get_na_urls(self):
        urls = ['http://{}:{}@{}.equityins.net/cgi-bin/qq.entry.py?agent={}'.format(u,self.PASSWORD,self.data["vdev"],u) for u in self.USRS]
        return urls

    def get_rewrite_urls(self):
        urls = [('http://' + u[0] + ':' + self.PASSWORD + '@' + self.data["vdev"] +
            '.equityins.net/cgi-bin/bbw.sh?pgm=POLICY&policyno=' + u[1])
            for u in zip(self.USRS,self.policies)]
        return urls

    def run_setup(self, urls, kwargs):
        """
    The master of puppets controls the browsers and soon
    Docker containers and someday The World!!!
        """
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

    def new_apps(self, urls):
        for u in urls:
            options = Options()
            options.add_argument("--devtools")
            driver = webdriver.Firefox(firefox_options=options)
            driver.get(u)
            
        
        # Open Chrome browsers in all 3 states and go to 
        # Quick Quote Rewrite Auto Rater
        for u in urls:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(chrome_options=options)
            driver.get(u)
            
    def main_loop(self):
        """
    Manages the UI.
        """
        while True:
            self.clear_screen()
            self.print_screen()
            print('Current vdev: {}'.format(self.data["vdev"]))
            self.print_main_menu()

            cmd = raw_input("\nEnter a command: ").strip().lower()

            if cmd == 'p':
                self.clear_screen()
                self.set_policies()

            elif cmd == 'v':
                self.clear_screen()
                self.set_vdev()

            elif cmd == 'r':
                try:
                    thread.start_new_thread(self.rewrites, (self.get_rewrite_urls(),))
                except Exception as e:
                    self.clear_screen()
                    traceback.print_exc()
                    print(type(e))
                    print(e)
                    print("Something went wrong! Try changing some data and continue.")

            elif cmd == 'n':
                    self.new_apps(self.get_na_urls())

            elif cmd == 'q':
               # self.clear_screen()
                print("Thanks for playing!")
                time.sleep(1)
               # self.clear_screen()
                sys.exit(0)
            elif cmd == 's':
                self.save_sfile()
            else:
                print("Try Again...")
                return self.main_loop()


    def print_screen(self):
        print('--------------------------------------------------------------')
        print("Today's Date: {}".format(self.today))
        print( 
            " _____                        _             \n"             
            "|  __ \                      | |            \n"            
            "| |__) _   _ _ __  _ __   ___| |_           \n"         
            "|  ___| | | | '_ \| '_ \ / _ | __|          \n"
            "| |   | |_| | |_) | |_) |  __| |_           \n"
            "|_|    \__,_| .__/| .__/ \___|\__|          \n"
            "            | |   | |                       \n"
            "            |_|_  |_|          _            \n"
            "            |  \/  |         | |            \n"
            "            | \  / | __ _ ___| |_ ___ _ __  \n"
            "            | |\/| |/ _` / __| __/ _ | '__| \n"
            "            | |  | | (_| \__ | ||  __| |    \n"
            "            |_|  |_|\__,_|___/\__\___|_|    \n"
            "--------------------------------------------------------------\n"
            "Welcome to Puppet Master {}".format(self.qa_specialist)                                 
                                             )
        print('--------------------------------------------------------------')
    
    def print_main_menu(self):
        print(
                "           MENU                    \n\n"
                ": r     -  Rewrites               :\n"
                ": n     -  New App                :\n"
                ": p     -  Enter New Policies     :\n"  
                ": v     -  Enter New Envirnoment  :\n"
                ": s     -  Save                   :\n"
                ": q     -  Quit                   :\n"
        )

    def clear_screen(self):
        print("\033c")


if __name__ == '__main__':
    a = App()
    a.main_loop()



