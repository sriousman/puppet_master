from selenium.webdriver.common.by import By


class DefaultAutoApplicatonLocators(object):

    CONTINUE_BUTTON = (By.XPATH, '// * [@id = "applform"] / p / input[3]')
    SAVE_BUTTON = (By.XPATH, '// * [@id = "applform"] / p / input[2]')
    EDIT_QUOTE_BUTTON = (By.XPATH, '// * [@id = "applform"] / p / input[1]')
    PAYMENT_PLAN_BUTTON = (By.ID, 'paybtn')

    PAYMENT_OPTION_SIXTH_DOWN = (By.XPATH, '//*[@id="payopt"]/tr[4]')

    OCCUPATION = (By.ID, '#dz1occ')
    EMPLOYER = (By.ID, '#dz1emp')

    # QUESTION_ONE_YES = 
    # QUESTION_ONE_NO
    # QUESTION_TWO_YES
    # QUESTION_TWO_NO
    # QUESTION_THREE_YES
    # QUESTION_THREE_NO
    # QUESTION_FOUR_YES
    # QUESTION_FOUR_NO
    # QUESTION_FIVE_YES
    # QUESTION_FIVE_NO
    # QUESTION_SIX_YES
    # QUESTION_SIX_NO
    # QUESTION_SEVEN_YES
    # QUESTION_SEVEN_NO
    # QUESTION_EIGHT_YES
    # QUESTION_EIGHT_NO
    # QUESTION_NINE_YES
    # QUESTION_NINE_NO
    # QUESTION_TEN_YES
    # QUESTION_TEN_NO
    # QUESTION_ELEVEN_YES
    # QUESTION_ELEVEN_NO
    # QUESTION_TWELVE_YES
    # QUESTION_TWELVE_NO