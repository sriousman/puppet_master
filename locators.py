from selenium.webdriver.common.by import By

class  QQRewriteARLocators(object):
    """
    A class for the Quick Quote Auto Rater page locators.
    """

    ADDRESS_BUTTON = (By.ID, 'address-button')

    # Address Modal
    MAILING_ADDRESS_INPUT = (By.ID, 'address-mailing-address')
    MAILING_APARTMENT_INPUT = (By.ID, 'address-mailing-apartment-number')
    MAILING_ZIPCODE_INPUT = (By.ID, 'address-mailing-zip')

    DIFF_ADDRESS_RADIO_YES = (By.XPATH, '//input[@name="optional-section-street"][@value="yes"]')
    DIFF_ADDRESS_RADIO_NO = (By.XPATH, '//input[@name="optional-section-street"][@value="no"]')

    STREET_ADDRESS_INPUT = (By.ID, 'address-street-address')
    STREET_APARTMENT_INPUT = (By.ID, 'address-street-apartment-number')
    STREET_ZIPCODE_INPUT = (By.ID, 'address-street-zip')

    DIFF_GARAGE_RADIO_YES = (By.XPATH, '//input[@name="optional-section-garaging"][@value="yes"]')
    DIFF_GARAGE_RADIO_NO = (By.XPATH, '//input[@name="optional-section-garaging"][@value="no"]')

    GARAGING_EXPLANATION = (By.NAME, 'explanation-garaging')

    SAVE_BUTTON = (By.XPATH, '//button[text()="Save"]')
    CANCEL_BUTTON = (By.XPATH, '//button[text()="Cancel"]')
    # End Address Modal
    
    EXIT_BUTTON = (By.ID, 'exit')
    RATE_BUTTON = (By.ID, 'rate')

