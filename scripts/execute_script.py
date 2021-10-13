# import webdriver
from selenium import webdriver

# create webdriver object
driver = webdriver.Chrome()

# get geeksforgeeks.org
driver.get("https://www.cultura.com/musique/genres-musicaux.html")

# # write script
# script = "alert('Alert via selenium')"
# driver.execute_script(script)

captcha_response = 'abc'
# driver.find_element_by_id('g-recaptcha-response').send_keys(captcha_response)
driver.execute_script("redemptionValidation(\"" + captcha_response + "\")")
