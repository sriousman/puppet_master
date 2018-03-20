from selenium.webdriver.common.by import By


class QQPremPayLocators(object):

    LICENSE_NUMBER = (By.ID, 'd1dln')
    
    LICENSE_STATE = (By.XPATH, '//*[@id="d1dls"]')
    
    APPLICATION_BUTTON = (By.ID, 'contbtn')
    
    EDIT_QUOTE_BUTTON = (By.XPATH, '//input[@value="Edit Quote"]')
