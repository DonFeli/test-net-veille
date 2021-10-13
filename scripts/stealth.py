from selenium import webdriver
from selenium_stealth import stealth
import time

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(executable_path="/Users/donor/PycharmProjects/scraping-tutorial-selenium/chromedriver",
                          options=options)

stealth(driver,
        languages=["en-US", "en"],
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/83.0.4103.53 Safari/537.36',
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
url = "https://www.cultura.com/musique/genres-musicaux.html?p=1"

driver.get(url)
print(driver.page_source)
time.sleep(5)
# driver.quit()


# search_input = driver.find_element_by_class_name("item")
# search_input.send_keys("My User Agent")

# driver.close()
