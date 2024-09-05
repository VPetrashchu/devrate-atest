
from pages.registration_page import RegistrationPage
from tests.config import driver


def test_successful_registration(driver):
    try:
        driver.get("http://localhost:3000")

        registration_page = RegistrationPage(driver)
        unique_email = registration_page.fill_registration_form()

        assert unique_email is not None
    finally:
        driver.quit()
