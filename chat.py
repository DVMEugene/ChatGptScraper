from settings import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from instructions import *
import time

def chat(driver, param):
    xpath = xpaths()
    textarea_locator = (By.XPATH, xpath['textarea'])
    textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located(textarea_locator))
    prompt = demographic_profile(param)
    print(f'User Input: {prompt}')
    textarea.send_keys(prompt)

