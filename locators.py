import pytest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set capabilities using AppiumOptions
options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "emulator-5554"  # command to Show connected device name 'adb devices'
# options.app_package = "com.android.settings"
# options.app_activity = ".Settings"
# options.language = "en"
# options.locale = "US"

appium_server_url = "http://localhost:4723/wd/hub"

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Remote(
        command_executor=appium_server_url,
        options=options
    )
    yield driver
    driver.quit()

def test_SearchIn_Chrome(driver):
    wait = WebDriverWait(driver, 30)
    try:
        el = wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'Chrome')))
        el.click()
        el1 = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[@text='Search or type web address']")))
        el1.send_keys('todays News')
         # Press the Enter key on the mobile keypad
        # wait.driver.press_keycode(66)
    except Exception as e:
        pytest.fail(f"Test failed due to: {str(e)}")