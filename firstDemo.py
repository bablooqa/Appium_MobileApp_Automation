import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options

# Set capabilities using AppiumOptions
options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "emulator-5554"  # command to Show connected device name 'adb devices'
options.app_package = "com.android.settings"
options.app_activity = ".Settings"
options.language = "en"
options.locale = "US"

appium_server_url = "http://localhost:4723/wd/hub"  
class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(
            command_executor=appium_server_url,
            options=options
        )

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_find_battery(self) -> None:
        el = self.driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Battery"]')
        el.click()
        # print("Battery found in battery directory:",el)

if __name__ == "__main__":
    unittest.main()