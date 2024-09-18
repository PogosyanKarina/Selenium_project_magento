import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import allure

# Constants
LOGIN_URL = "https://magento.softwaretestingboard.com/customer/account/login/"
ACCOUNT_URL = "https://magento.softwaretestingboard.com/customer/account/"
EMAIL = "pogosyankv84@gmail.com"
PASSWORD = "karina1234$"
NEW_PASSWORD = "karina1234$"


@pytest.fixture(scope='module')
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration
    chrome_options.add_argument("--no-sandbox")  # Disables sandboxing
    chrome_options.add_argument("--window-size=1920,1000")
    driver = webdriver.Chrome(options=chrome_options)

    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.mark.regression
@allure.feature('Login')
@allure.story('Invalid login')
@allure.title('Test invalid login attempt')
def test_invalid_login(driver):
    with allure.step('Navigate to login page'):
        driver.get(LOGIN_URL)

    with allure.step('Enter invalid email and password'):
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys("invalidemail@gmail.com")

        password_input = driver.find_element(By.ID, 'pass')
        password_input.send_keys('invalid_password')

    with allure.step('Click login button'):
        login_button = driver.find_element(By.ID, 'send2')
        login_button.click()

    time.sleep(3)

    with allure.step('Verify error message'):
        error_message = driver.find_element(By.XPATH, "//div[contains(@class, 'message-error')]")
        assert "Please wait and try again later" in error_message.text


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature('Login')
@allure.story('Successful login')
@allure.title('Test successful login')
def test_login(driver):
    with allure.step('Navigate to login page'):
        driver.get(LOGIN_URL)

    with allure.step('Enter valid email and password'):
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys(EMAIL)

        password_input = driver.find_element(By.ID, "pass")
        password_input.send_keys(PASSWORD)

    with allure.step('Click login button'):
        login_button = driver.find_element(By.ID, "send2")
        login_button.click()

    time.sleep(3)

    with allure.step('Verify successful login'):
        assert driver.current_url == ACCOUNT_URL


@pytest.mark.regression
@allure.feature('Change Password')
@allure.story('Change password with incorrect current password')
@allure.title('Test change password with incorrect current password')
def test_change_password_incorrect_current(driver):
    with allure.step('Navigate to account page'):
        driver.get(ACCOUNT_URL)

    with allure.step('Click on Change Password link'):
        change_password_link = driver.find_element(By.LINK_TEXT, "Change Password")
        change_password_link.click()

    with allure.step('Enter incorrect current password and new password'):
        current_password_input = driver.find_element(By.ID, "current-password")
        current_password_input.send_keys('incorrect_password')

        new_password_input = driver.find_element(By.ID, "password")
        new_password_input.send_keys(NEW_PASSWORD)

        confirm_password_input = driver.find_element(By.ID, "password-confirmation")
        confirm_password_input.send_keys(NEW_PASSWORD)

    with allure.step('Click Save button'):
        save_button = driver.find_element(By.XPATH, "//button[@title='Save']")
        save_button.click()

    time.sleep(3)

    with allure.step('Verify error message for incorrect current password'):
        error_message = driver.find_element(By.XPATH, "//div[contains(@class, 'message-error')]")
        assert "The password doesn't match this account." in error_message.text


@pytest.mark.regression
@allure.feature('Change Password')
@allure.story('Change password with mismatched confirmation')
@allure.title('Test change password with mismatched confirmation')
def test_change_mismatch(driver):
    with allure.step('Navigate to account page'):
        driver.get(ACCOUNT_URL)

    with allure.step('Click on Change Password link'):
        change_password_link = driver.find_element(By.LINK_TEXT, "Change Password")
        change_password_link.click()

    with allure.step('Enter current and new passwords, with mismatched confirmation'):
        current_password_input = driver.find_element(By.ID, "current-password")
        current_password_input.send_keys(PASSWORD)

        new_password_input = driver.find_element(By.ID, "password")
        new_password_input.send_keys(NEW_PASSWORD)

        confirm_password_input = driver.find_element(By.ID, "password-confirmation")
        confirm_password_input.send_keys("mismatched_password")

    with allure.step('Click Save button'):
        save_button = driver.find_element(By.CSS_SELECTOR, ".action.save.primary")
        save_button.click()

    time.sleep(3)

    with allure.step('Verify error message for mismatched password confirmation'):
        error_message = driver.find_element(By.ID, "password-confirmation-error")
        assert "Please enter the same value again." in error_message.text


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature('Change Password')
@allure.story('Successful password change')
@allure.title('Test successful password change')
def test_change_password(driver):
    with allure.step('Navigate to account page'):
        driver.get(ACCOUNT_URL)

    with allure.step('Click on Change Password link'):
        change_password_link = driver.find_element(By.LINK_TEXT, "Change Password")
        change_password_link.click()

    with allure.step('Enter current and new passwords'):
        current_password_input = driver.find_element(By.ID, "current-password")
        current_password_input.send_keys(PASSWORD)

        new_password_input = driver.find_element(By.ID, "password")
        new_password_input.send_keys(NEW_PASSWORD)

        confirm_password_input = driver.find_element(By.ID, "password-confirmation")
        confirm_password_input.send_keys(NEW_PASSWORD)

    with allure.step('Click Save button'):
        save_button = driver.find_element(By.XPATH, "//button[@title='Save']")
        save_button.click()

    with allure.step('Verify success message'):
        success_message = driver.find_element(By.XPATH, "//div[contains(@class, 'message-success')]")
        assert 'You saved the account information.' in success_message.text
