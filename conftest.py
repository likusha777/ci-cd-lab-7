import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")

    # В CI/CD нет экрана, а задача выполняется в контейнере от root,
    # поэтому браузер запускается без окна и без sandbox.
    # Локально (переменная HEADLESS не задана) Chrome открывается как обычно.
    if os.environ.get("HEADLESS") == "1":
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    driver.implicitly_wait(5)

    yield driver

    driver.quit()


@pytest.fixture
def base_url():
    return "https://ya.ru"
