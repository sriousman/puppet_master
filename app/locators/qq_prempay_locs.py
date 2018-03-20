from selenium.webdriver.common.by import By


class QQPremPayLocators(object):

    APPLICATION_BUTTON = (By.XPATH, '//input[@value="Application »"]')
    QUOTE_DETAIL_BUTTON = (By.ID, 'btnShow')
    EDIT_QUOTE_BUTTON = (By.XPATH, '//input[@value="« Edit Quote"]')


