import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy


capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    # appPackage='com.android.settings',
    # appActivity='.Settings',
    # language='en',
    # locale='US',
    language='zh',
    locale='CN'
)

appium_server_url = 'http://localhost:4723'
driver = webdriver.Remote(appium_server_url, capabilities)

# Copy inspector code
# driver.press_keycode(3, undefined, undefined);
driver.back()
el1 = driver.find_element(by=AppiumBy.XPATH, value="//android.widget.ImageView[@content-desc=\"微信\"]")
el1.click()



driver.quit()


