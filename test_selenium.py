import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://127.0.0.1:5000"


def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    chrome_bin = os.environ.get("CHROME_BIN")
    if chrome_bin:
        options.binary_location = chrome_bin

    # webdriver-manager downloads a chromedriver build that matches
    # whatever Chrome is actually installed, checked at run time --
    # avoids version-mismatch errors between Chrome and chromedriver.
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def fill_and_submit(driver, url, username, password):
    driver.get(url)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(1)


def test_weak_password_rejected_on_login():
    driver = get_driver()
    try:
        fill_and_submit(driver, BASE_URL, "testuser", "password")
        assert "Welcome" not in driver.page_source, "common password was wrongly accepted"
    finally:
        driver.quit()


def test_strong_password_accepted_on_login():
    driver = get_driver()
    try:
        fill_and_submit(driver, BASE_URL, "testuser", "Correct-Horse-Battery-Staple-99")
        assert "Welcome" in driver.page_source, "strong password was wrongly rejected"
    finally:
        driver.quit()


def test_account_creation_with_strong_password():
    driver = get_driver()
    try:
        fill_and_submit(driver, f"{BASE_URL}/register", "new_test_user", "Zx9!Quartz-Meridian")
        assert "Welcome" in driver.page_source, "registration with a strong password should succeed"
    finally:
        driver.quit()


if __name__ == "__main__":
    test_weak_password_rejected_on_login()
    print("weak password correctly rejected on login")
    test_strong_password_accepted_on_login()
    print("strong password correctly accepted on login")
    test_account_creation_with_strong_password()
    print("account creation correctly logged and accepted")