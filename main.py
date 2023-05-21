
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from settings import *
from auth import auth
from chat import chat

import time
import psutil

def stop_chrome_processes():
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'chrome.exe':
            process.kill()
            print(f"Stopped process with PID {process.pid} - {process.info['name']}")

def user_input():
    keyword = "facebook ads for real estate agents"
    search_intent = "informational"
    param = {
        'keyword': keyword,
        'search_intent': search_intent,
    }
    return param

def main():
    driver = chrome_config()  # Proxy enabled
    # driver = non_proxy()
    model = gpt_models()
    # navigating to a page
    driver.get(f'https://chat.openai.com/{model["gpt3.5"]}')
    xpath = xpaths()

    if driver.find_element(By.XPATH, xpath['textarea']):
        print("Your In Chat GPT!")
        chat(driver, user_input())
    else:
        login_button_locator = (By.XPATH, xpath['button_login'])

        for i in range(3):  # Retry clicking the button 3 times
            try:
                login_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(login_button_locator))
                print("Element to click:", login_button)
                login_button.click()
                auth(driver)  # start login session

                break  # If the click is successful, break out of the loop
            except TimeoutException:
                print(f"Attempt {i + 1} failed. Button was not clickable, retrying...")
                if i == 2:  # Check if it's the last iteration (indices start at 0)
                    print("Skipping after 3 failed attempts.")
                time.sleep(2)  # Wait 2 seconds before retrying

    # Simulate Esc key press to stop page loading
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    # Infinite loop to keep the script running
    while True:
        time.sleep(1)


if __name__ == "__main__":
    stop_chrome_processes()  # if chrome driver not working run this
    main()
