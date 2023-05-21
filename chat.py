from settings import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, InvalidSelectorException

from instructions import *
import time
from sqlite import setup_db

def chat(driver, param):
    xpath = xpaths()
    textarea_locator = (By.XPATH, xpath['textarea'])
    textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located(textarea_locator))
    prompt = demographic_profile(param)
    print(f'User Input: {prompt}')
    textarea.send_keys(prompt)

    get_response(driver)


def get_response(driver):
    conn, c = setup_db()
    response_texts = []  # create a list to store the response texts
    response_base_xpath = '//div[@class="markdown prose w-full break-words dark:prose-invert light"]'  # corrected here
    done_xpath = '//*[@id="__next"]/div[2]/div[2]/div/main/div[3]/form/div/div[1]/div/button'
    done_locator = (By.XPATH, done_xpath)
    response_index = 2  # start from the first response
    while True:
        response_locator = (By.XPATH, response_base_xpath)
        try:
            response = WebDriverWait(driver, 20).until(EC.presence_of_element_located(response_locator))
            response_text = response.text
            if len(response_texts) == 0 or response_text != response_texts[-1]:  # if response is different from the last one
                response_texts.append(response_text)  # append the response text to the list
                print("\n".join(response_texts))  # print the entire response string so far
                c.execute("INSERT INTO content (text) VALUES (?)", (response_text,))  # save the text into the database
                conn.commit()
            response_index += 2  # prepare for the next response
        except TimeoutException:
            print("No new response found after waiting for 10 seconds.")
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(done_locator))
                print("Writing is done.")
                # break  # exit the loop when writing is done
            except TimeoutException:
                print("Writing is still in progress.")
        except InvalidSelectorException:  # handle invalid selector exception
            print("Invalid XPATH selector, trying again.")
            continue
        time.sleep(5)  # wait for 5 seconds
    conn.close()
