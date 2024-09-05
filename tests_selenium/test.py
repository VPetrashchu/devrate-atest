from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests
import re
import imaplib
import email

def get_latest_email():
    MAILHOG_API_URL = "http://127.0.0.1:8025/api/v2/messages"
    try:
        response = requests.get(MAILHOG_API_URL)
        response.raise_for_status()

        messages = response.json().get('items', [])
        if not messages:
            print('No messages found.')
            return None

        latest_message = messages[0]
        return latest_message

    except requests.RequestException as e:
        print(f"Error fetching messages: {e}")
        return None
def read_last_email_counter(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return int(file.read().strip())
    return 0


def write_last_email_counter(filename, counter):
    with open(filename, 'w') as file:
        file.write(str(counter))


def generate_unique_email(base_email, counter):
    return f"{base_email.split('@')[0]}+{counter}@{base_email.split('@')[1]}"


# Функція для отримання коду підтвердження з електронної пошти
def get_confirmation_code():
    MAILHOG_API_URL = "http://127.0.0.1:8025/api/v2/messages"
    try:
        response = requests.get(MAILHOG_API_URL)
        response.raise_for_status()

        messages = response.json().get('items', [])

        if not messages:
            print('No messages found.')
            return None

        # Вибір найбільш актуального повідомлення, якщо їх кілька
        latest_message = messages[0]
        body = latest_message['Content']['Body']

        # Пошук коду підтвердження
        code = re.search(r'\b\d{6}\b', body)
        if code:
            return code.group(0)
        else:
            print('Confirmation code not found.')
            return None
    except requests.RequestException as e:
        print(f"Error fetching messages: {e}")
        return None


def use_selenium():
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/google-chrome"  # шлях до вашого браузера Chrome
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("http://localhost:3000")  # Змініть на URL, який ви використовуєте

    wait = WebDriverWait(driver, 15)
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="MuiBox-root css-i1tlby"]')))
    dropdown.click()

    counter_file = 'email_counter.txt'
    email_counter = read_last_email_counter(counter_file) + 1
    write_last_email_counter(counter_file, email_counter)

    base_email = "vasi.pet.m@gmail.com"
    unique_email = generate_unique_email(base_email, email_counter)

    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys(unique_email)

    button = driver.find_element(By.CSS_SELECTOR, 'button[title="Open"]')
    button.click()

    option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//li[contains(@class, "MuiAutocomplete-option") and contains(text(), "Andorra")]')))
    option.click()

    name_input = driver.find_element(By.NAME, "firstName")
    name_input.send_keys("test")

    surname_input = driver.find_element(By.NAME, "lastName")
    surname_input.send_keys("test")

    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys("Qwerty1!")

    repeat_password_input = driver.find_element(By.NAME, "repeatPassword")
    repeat_password_input.send_keys("Qwerty1!")

    checkbox_news = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="news" and @type="checkbox"]')))
    driver.execute_script("arguments[0].scrollIntoView();", checkbox_news)
    if not checkbox_news.is_selected():
        checkbox_news.click()

    checkbox_agreement = wait.until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="agreement" and @type="checkbox"]')))
    driver.execute_script("arguments[0].scrollIntoView();", checkbox_agreement)
    if not checkbox_agreement.is_selected():
        checkbox_agreement.click()

    button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "MuiButtonBase-root") and @type="submit"]')))
    button.click()

    # Надсилання форми для отримання коду підтвердження
    submit_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "MuiButtonBase-root") and @type="submit"]')))
    submit_button.click()

    # Пауза для того, щоб код підтвердження був надісланий
    time.sleep(20)  # Збільшення часу очікування, якщо потрібно

    # Отримання коду підтвердження з електронної пошти
    confirmation_code = get_confirmation_code()

    if confirmation_code:
        print(f"Confirmation Code: {confirmation_code}")  # Вивести код підтвердження в консоль

        for i, digit in enumerate(confirmation_code):
            # Знаходження наступного div класу `MuiFormControl-root`
            input_xpath = f'//div[@class="MuiBox-root css-52akdr"]/div[{i + 1}]//input'
            input_field = wait.until(EC.presence_of_element_located((By.XPATH, input_xpath)))
            input_field.send_keys(digit)

        # Кнопка підтвердження
        confirm_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[contains(@class, "MuiButtonBase-root") and @type="submit"]')))
        confirm_button.click()

        # Додатковий час очікування перед закриттям
        time.sleep(15)
    else:
        print("Confirmation code was not retrieved. Exiting...")

    # Логін

    email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    email_input.send_keys(unique_email)

    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys("Qwerty1!")

    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "MuiButtonBase-root") and @type="submit"]')))
    login_button.click()

    # Додатковий час для завершення логіну
    time.sleep(15)
    driver.quit()


if __name__ == "__main__":
    use_selenium()
