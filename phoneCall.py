import pytest
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set capabilities using UiAutomator2Options
options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "emulator-5554"  # Command to show connected device name 'adb devices'
options.app_package = "com.google.android.dialer"
options.app_activity = "com.android.dialer.main.impl.MainActivity"
options.language = "en"
options.locale = "US"

appium_server_url = "http://localhost:4723/wd/hub"

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Remote(
        command_executor=appium_server_url,
        options=options
    )
    yield driver
    driver.quit()

def enter_phone_number(driver, phone_number):
    """Function to enter a phone number digit by digit on the dial pad."""
    for digit in phone_number:
        xpath = f'//*[@text="{digit}"]'
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        el.click()
        time.sleep(1)  # Adding a small delay between clicks to mimic real user interaction

def dialing_call(driver):
    """Function to click the dial button."""
    el = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'dial'))
    )
    el.click()

def end_call(driver):
    """Function to click the end call button."""
    el = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'End call'))
    )
    el.click()

def test_phoneCall_dialler(driver) -> None:
    # Click on 'Recents' tab
    el = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="Recents"]')
    el.click()
    time.sleep(3)
    
    # Click on 'key pad' button
    key_pad = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='key pad')
    key_pad.click()
    time.sleep(3)
    
    # Enter the phone number
    phone_number = "7888632265"
    enter_phone_number(driver, phone_number)
    time.sleep(3)
    
    # Click the dial button
    dialing_call(driver)
    time.sleep(5)  # Assuming some time for the call to be connected
    
    # End the call
    end_call(driver)
    time.sleep(3)