from selenium.webdriver.common.by import By

class  QRWAutoRaterLocators(object):
    """
    A class for the Quick Quote Auto Rater page locators.
    """

    # BUTTONS
    RATE_BUTTON = (By.ID, 'rate')
    EXIT_BUTTON = (By.ID, 'exit')

    ADDRESS_BUTTON = (By.ID, 'addresses-button')
