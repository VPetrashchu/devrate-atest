from selenium.webdriver.common.by import By

class RegistrationLocators:
    DROPDOWN = (By.XPATH, '//div[@class="MuiBox-root css-i1tlby"]')
    EMAIL_INPUT = (By.NAME, "email")
    OPEN_BUTTON = (By.CSS_SELECTOR, 'button[title="Open"]')
    OPTION_ANDORRA = (By.XPATH, '//li[contains(@class, "MuiAutocomplete-option") and contains(text(), "Andorra")]')
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    PASSWORD_INPUT = (By.NAME, "password")
    REPEAT_PASSWORD_INPUT = (By.NAME, "repeatPassword")
    NEWS_CHECKBOX = (By.XPATH, '//input[@name="news" and @type="checkbox"]')
    AGREEMENT_CHECKBOX = (By.XPATH, '//input[@name="agreement" and @type="checkbox"]')
    SUBMIT_BUTTON = (By.XPATH, '//button[contains(@class, "MuiButtonBase-root") and @type="submit"]')
