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
options.app_package = "com.google.android.contacts"
options.app_activity = "com.google.android.apps.contacts.activities.PeopleActivity"
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

def accept_notification_permission(driver):
    try:
        allow_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.Button[@text="Allow"]'))
        )
        allow_button.click()
    except Exception as e:
        print(f"Notification permission dialog not found: {e}")

def test_create_contact(driver):
    accept_notification_permission(driver)
    
    # Wait for the "Create contact" button and click it
    try:
        create_contact_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.ImageButton[@content-desc="Create contact"]'))
        )
        create_contact_button.click()
    except Exception as e:
        print(f"Create contact button not found: {e}")
    
    # Wait for a few seconds to observe the result
    time.sleep(3)