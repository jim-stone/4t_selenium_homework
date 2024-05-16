import os
import pytest
from dotenv import load_dotenv
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages import LoginPage

load_dotenv()

@pytest.fixture
def chrome_browser():
    service = Service(ChromeDriverManager().install())
    browser = Chrome(service=service)
    browser.set_window_size(1920, 1080)
    yield browser
    browser.quit()

@pytest.fixture
def logged_in(chrome_browser):
    login = os.getenv('ADM_MAIL')
    password = os.getenv('ADM_PASS')
    LoginPage(browser=chrome_browser).open().login(login, password)
    yield chrome_browser


