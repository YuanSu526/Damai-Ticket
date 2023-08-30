# @credit to 青灯教育
# This version is an updated and modified version of the original auther
# Modified the code so that it is executable on the current version of damai.cn
# Optimized the code so that it will remain on the purchasing page until the ticket becomes available


import time
from info import PHONE, PASSWORD, NAME, NAME2
from selenium import webdriver
from selenium.webdriver.common. by import By

# Basic configuration
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
prefs = {'credentials_enable_service': False, 'profile.password_manager_enabled': False}
options.add_experimental_option('prefs', prefs)
options.add_argument('--disable-blink-features=AutomationControlled')

# Open Google Chrome and go to damai.cn
driver = webdriver.Chrome(options=options)
f = open('stealth.min.js', mode='r', encoding='utf-8').read()
# Remove the crawler aspect on selenium
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': f})
driver.get('https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F')

# Log in
driver.switch_to.frame(0)
# Enter User Id and Password
driver.find_element(By.XPATH, '//*[@id="fm-login-id"]').send_keys(PHONE)
driver.find_element(By.XPATH, '//*[@id="fm-login-password"]').send_keys(PASSWORD)
time.sleep(0.5)

# If a slider for user identification appeared
try:
    # Click and hold onto the slider, release after 0.5 seconds
    time.sleep(1)
    driver.switch_to.frame(0)
    time.sleep(1)
    slider = driver.find_element(By.XPATH, '//*[@id="nc_1_n1z"]')
    # Distance to slide over: 300-42=258
    webdriver.ActionChains(driver).click_and_hold(on_element=slider).perform()
    webdriver.ActionChains(driver).move_by_offset(xoffset=258, yoffset=0).perform()
    webdriver.ActionChains(driver).pause(0.5).release().perform()
    driver.switch_to.parent_frame()
except:
    print('Skipping slider')
# Click log in
driver.find_element(By.XPATH, '//*[@id="login-form"]/div[4]/button').click()
time.sleep(0.5)

# Go to the target ticket item
target_url = 'https://detail.damai.cn/item.htm?spm=a2oeg.home.card_2.ditem_5.258c23e1dR1efJ&id=725907479664'
driver.get(target_url)

# Executing the purchasing action sequence
# ！！！Some ticket item may not support website purchase
availableToPurchase = False
while not availableToPurchase:
    try:
        # Try clicking purchase
        driver.find_element(By.XPATH, '//div[@class="buybtn"]').click()
        availableToPurchase = True
    except:

        try:
            # Try clicking another format of purchase
            driver.find_element(By.XPATH, '//div[@class="buy-link"]').click()
            availableToPurchase = True
        except:

            try:
                # If this item does not support website purchase
                driver.find_element(By.XPATH, '//div[@class="dunsale"]')
                print('Not available to purchasing online, exit')
                exit()
            except:
                # Other conditions, assume the ticket is not available to purchase yet, refresh page
                driver.refresh()
                print('Waiting...')

# Entering the purchasing page, enter user info
time.sleep(1)
# Selecting ID card

clicked = False
while not clicked:
    try:
        element = driver.find_element(By.XPATH, "//div[@id='app']/div[@id='confirmOrder_1']/div[@id='dmViewerBlock_DmViewerBlock']/div[@class='viewer']/div/div[1]/div[3]/i").click()
        clicked = True
    except:
        print('Try clicking ID card again')

# Entering audience name
driver.find_element(By.XPATH, "//div[@id='app']/div[@id='confirmOrder_1']/div[@id='dmContactBlock_DmContactBlock']/div[2]/div/div/input").clear()
driver.find_element(By.XPATH, "//div[@id='app']/div[@id='confirmOrder_1']/div[@id='dmContactBlock_DmContactBlock']/div[2]/div/div/input").send_keys(NAME)

#Every information entered
print('Every information entered, please click on purchase manually to do the final purchase')
