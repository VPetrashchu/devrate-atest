from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from core.locators.registration_locators import RegistrationLocators
from core.email_utils import generate_unique_email, read_last_email_counter, write_last_email_counter
from tests.config import BASE_EMAIL, COUNTER_FILE

class RegistrationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def fill_registration_form(self):
        dropdown = self.wait.until(EC.element_to_be_clickable(RegistrationLocators.DROPDOWN))
        dropdown.click()

        email_counter = read_last_email_counter(COUNTER_FILE) + 1
        write_last_email_counter(COUNTER_FILE, email_counter)

        unique_email = generate_unique_email(BASE_EMAIL, email_counter)

        email_input = self.driver.find_element(*RegistrationLocators.EMAIL_INPUT)
        email_input.send_keys(unique_email)

        button = self.driver.find_element(*RegistrationLocators.OPEN_BUTTON)
        button.click()

        option = self.wait.until(EC.element_to_be_clickable(RegistrationLocators.OPTION_ANDORRA))
        option.click()

        name_input = self.driver.find_element(*RegistrationLocators.FIRST_NAME_INPUT)
        name_input.send_keys("test")

        surname_input = self.driver.find_element(*RegistrationLocators.LAST_NAME_INPUT)
        surname_input.send_keys("test")

        password_input = self.driver.find_element(*RegistrationLocators.PASSWORD_INPUT)
        password_input.send_keys("Qwerty1!")

        repeat_password_input = self.driver.find_element(*RegistrationLocators.REPEAT_PASSWORD_INPUT)
        repeat_password_input.send_keys("Qwerty1!")

        checkbox_news = self.wait.until(EC.presence_of_element_located(RegistrationLocators.NEWS_CHECKBOX))
        self.driver.execute_script("arguments[0].scrollIntoView();", checkbox_news)
        if not checkbox_news.is_selected():
            checkbox_news.click()

        checkbox_agreement = self.wait.until(EC.presence_of_element_located(RegistrationLocators.AGREEMENT_CHECKBOX))
        self.driver.execute_script("arguments[0].scrollIntoView();", checkbox_agreement)
        if not checkbox_agreement.is_selected():
            checkbox_agreement.click()

        button = self.wait.until(EC.element_to_be_clickable(RegistrationLocators.SUBMIT_BUTTON))
        button.click()

        submit_button = self.wait.until(EC.element_to_be_clickable(RegistrationLocators.SUBMIT_BUTTON))
        submit_button.click()

        time.sleep(20)

        return unique_email
