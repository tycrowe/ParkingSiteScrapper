from selenium import webdriver
from pathlib import Path
from selenium.webdriver.common.by import By
import os

parking_site = "https://parkingavailability.uncc.edu/"
chromedriverpath = str(Path(__file__).resolve().parents[0])
chromedriverpath += "\\chromedriver.exe"
if not os.path.isfile(chromedriverpath):
    print("CHROMEDRIVER NOT INSTALLED, PLEASE DROP CHROMEDRIVER.EXE INTO EXECUTING DIRECTORY.")
    print("Download file here: https://sites.google.com/a/chromium.org/chromedriver/downloads")
else:
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    browser = webdriver.Chrome(chromedriverpath, chrome_options=options)
    browser.get(parking_site)
    decks = browser.find_elements_by_class_name("deck-name")
    percents = browser.find_elements(By.XPATH, "//div[contains(@class, 'green') or "
                                               "contains(@class, 'yellow') or "
                                               "contains(@class, 'red') and "
                                               "contains(@class, 'ng-star-inserted')"
                                               "]")
    for x in range(0, len(decks)):
        print(str(decks[x].get_attribute("innerHTML")) + str(percents[x].get_attribute("innerHTML")))