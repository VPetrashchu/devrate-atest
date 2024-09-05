import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


# @pytest.fixture(scope="function")
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/google-chrome"
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    yield driver

    driver.quit()

BASE_EMAIL = "vasi.pet.m@gmail.com"
COUNTER_FILE = 'email_counter.txt'

