import os
import random
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
load_dotenv('./secrets/.env')

def xpaths():
    textarea = '//textarea[@id="prompt-textarea"]'
    button_login = '//*[@id="__next"]/div[1]/div[1]/div[4]/button[1]/div'
    username = '//input[@id="username"]'
    login_submit = '//button[@type="submit"]'
    password = '//input[@id="password"]'

    xpath = {
        'textarea': textarea,
        'button_login': button_login,
        'username': username,
        'password': password,
        'login_submit': login_submit,
    }
    return xpath

def gpt_models():
    param = {
        'gpt4': "?model=gpt-4",
        'gpt3.5': "?model=3.5%20turbo"
    }
    return param

def chrome_config():
    proxy_settings = proxies()
    # Choose the webdriver for the browser you want (e.g., Firefox, Chrome)
    # Make sure the webdriver is installed and available in the system path
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    # Configure the proxy
    chrome_options.add_argument(
        f"https://{proxy_settings['proxy_username']}:{proxy_settings['proxy_password']}@{proxy_settings['proxy_server']}:{proxy_settings['proxy_port']}"
    )
    chrome_options.add_argument(
        f"http://{proxy_settings['proxy_username']}:{proxy_settings['proxy_password']}@{proxy_settings['proxy_server']}:{proxy_settings['proxy_port']}"
    )

    prefs = {
        "profile.default_content_setting_values.notifications": 2,  # Block all notifications
        "profile.default_content_setting_values.popups": 2,  # Block all popups
        "profile.default_content_settings.state.popups": 2,
        "profile.default_content_setting_values.automatic_downloads": 1  # Allow automatic downloads
    }
    chrome_options.add_experimental_option("prefs", prefs)

    chrome_options.user_data_dir = "C:/Users/billi/AppData/Local/Google/Chrome/User Data"

    # service = Service(executable_path=chromedriver_filename)

    driver = uc.Chrome(options=chrome_options)

    return driver


def non_proxy():
    chrome_options = Options()
    chrome_options.add_argument('--no-first-run')
    chrome_options.add_argument('--no-service-autorun')
    chrome_options.add_argument('--password-store=basic')

    prefs = {
        "profile.default_content_setting_values.notifications": 2,  # Block all notifications
        "profile.default_content_setting_values.popups": 2,  # Block all popups
        "profile.default_content_settings.state.popups": 2,
        "profile.default_content_setting_values.automatic_downloads": 1  # Allow automatic downloads
    }
    chrome_options.add_experimental_option("prefs", prefs)

    chrome_options.add_argument("--user-data-dir=/Users/billi/AppData/Local/Google/Chrome/User Data")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def randomize_port(existing_port):
    new_port = random.randint(1024, 65535)
    while new_port == existing_port:
        new_port = random.randint(1024, 65535)
    return new_port

def proxies():
    # Configure the proxy server and port
    proxy_server = os.getenv("PROXY_SERVER")
    proxy_port = os.getenv("PROXY_PORT")
    proxy_username = os.getenv("PROXY_USERNAME")
    proxy_password = os.getenv("PROXY_PASSWORD")
    gpt_username = os.getenv("GPT_USERNAME")
    gpt_password = os.getenv("GPT_PASSWORD")

    if proxy_port:
        proxy_port = int(proxy_port)
        proxy_port = randomize_port(proxy_port)
        print(proxy_port)

    proxy_settings = {
        'proxy_server': proxy_server,
        'proxy_port': proxy_port,
        'proxy_username': proxy_username,
        'proxy_password': proxy_password,
        'gpt_username': gpt_username,
        'gpt_password': gpt_password
    }

    return proxy_settings

