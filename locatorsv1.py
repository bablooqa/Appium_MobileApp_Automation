import os
import time
import pytest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Ensure the Screenshots directory exists
if not os.path.exists('Screenshots'):
    os.makedirs('Screenshots')

options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "emulator-5554"
options.no_reset = True  # Add this option to avoid resetting the app state between runs

appium_server_url = "http://localhost:4723/wd/hub"

@pytest.fixture(scope="function")
def driver():
    print("Initializing Appium driver...")
    driver = webdriver.Remote(
        command_executor=appium_server_url,
        options=options
    )
    yield driver
    print("Quitting Appium driver...")
    driver.quit()

def capture_screenshot(driver, name):
    screenshot_path = f"Screenshots/{name}.png"
    print(f"Capturing screenshot: {screenshot_path}")
    driver.save_screenshot(screenshot_path)

def test_SearchIn_Chrome(driver):
    wait = WebDriverWait(driver, 60)  # Increase wait time if needed
    try:
        print("Clicking Chrome app...")
        el = wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'Chrome')))
        el.click()
    
        # Capture screenshot after clicking Chrome
        capture_screenshot(driver, "chrome_launched")
    
        print("Waiting for Chrome to load...")
        time.sleep(10)  # Initial wait for Chrome to fully load
    
        # Try different locator strategies for the search box
        print("Searching for the search box...")
        search_box = None
        attempts = 0
        max_attempts = 5

        while not search_box and attempts < max_attempts:
            try:
                search_box = wait.until(
                    EC.presence_of_element_located((AppiumBy.XPATH, "//input[@type='text']"))
                )
            except Exception as e:
                print(f"Search box not found. Attempt {attempts + 1}/{max_attempts}. Error: {e}")
                capture_screenshot(driver, f"attempt_{attempts + 1}")
                time.sleep(5)  # Additional wait before retrying
                attempts += 1
        
        if not search_box:
            search_box = wait.until(
                EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
            )
        
        print("Found search box, entering text...")
        search_box.send_keys('todays News')
        capture_screenshot(driver, "after_entering_text")
    
        print("Pressing Enter key...")
        driver.press_keycode(66)
        capture_screenshot(driver, "after_pressing_enter")
    
    except Exception as e:
        capture_screenshot(driver, "error_state")
        pytest.fail(f"Test failed due to: {str(e)}")

if __name__ == "__main__":
    print("Running the test...")
    pytest.main()
    print("Test run complete.")