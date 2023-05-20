from settings import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv
import time
load_dotenv('./secrets/.env')

def auth(driver):
    proxy = proxies()
    xpath = xpaths()
    username_locator = (By.XPATH, xpath['username'])
    password_locator = (By.XPATH, xpath['password'])
    login_location = (By.XPATH, xpath['login_submit'])
    for i in range(3):  # Retry clicking the button 3 times
        try:
            # Username
            username = WebDriverWait(driver, 10).until(EC.presence_of_element_located(username_locator))
            username.clear()

            if proxy['gpt_username'] is None:
                print("gpt_username is not set. Please check your environment variables.")
            else:
                username.send_keys(proxy['gpt_username'])

            # Login button
            login_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(login_location))
            login_button.click()

            # Password
            password = WebDriverWait(driver, 10).until(EC.presence_of_element_located(password_locator))
            password.clear()

            if proxy['gpt_password'] is None:
                print("gpt_password is not set. Please check your environment variables.")
            else:
                password.send_keys(proxy['gpt_password'])

            # Login button
            login_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(login_location))
            login_button.click()

            break  # If the click is successful, break out of the loop
        except TimeoutException:
            print(f"Attempt {i + 1} failed. Button was not clickable, retrying...")
            if i == 2:  # Check if it's the last iteration (indices start at 0)
                print("Skipping after 3 failed attempts.")
            time.sleep(2)  # Wait 2 seconds before retrying

