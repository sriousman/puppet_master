from selenium.webdriver.common.by import By

class  QQEntryLocators(object):
    """
    A class for the Quick Quote Auto Rater page locators.
    """

    # BUTTONS
    CONTACT_INFO_BUTTON = (By.ID, 'contact-info')
    CANCEL_BUTTON = (By.XPATH, '//p/input[@value="Cancel"]')
    SAVE_BUTTON = (By.XPATH, '//p/input[@value="Save"]')
    RATE_BUTTON = (By.XPATH, '//input[@value="Rate"]')

    # INPUTS

    LASTNAME = (By.XPATH, '//input[@id="insName"]')
    ZIPCODE = (By.XPATH, '//input[@id="street-zip-base"]')
    AGENCY_FEE = (By.ID, 'agencyFee')
    FIRSTNAME = (By.XPATH, ('//*[@id="firstname/OID(0)"]'))
    BIRTHDATE = (By.XPATH, ('//*[@id="birthdate/OID(0)"]'))
    VIN = (By.XPATH, ('//*[@id="vin/OID(0)"]'))
    YEAR = (By.XPATH, ('//*[@id="year/OID(0)"]'))
