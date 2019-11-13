#!/usr/bin/env python2

from selenium import webdriver
from pathlib import Path
from selenium.webdriver.common.by import By
import os
from datetime import datetime
import mysql.connector
import pytz

parking_site = "https://parkingavailability.uncc.edu/"
chromedriverpath = str(Path(__file__).resolve().parents[0])
chromedriverpath += "/chromedriver.exe"
print("CHROMEDRIVER PATH: " + str(chromedriverpath))
if not os.path.isfile(chromedriverpath):
    print("CHROMEDRIVER NOT INSTALLED, PLEASE DROP CHROMEDRIVER.EXE INTO EXECUTING DIRECTORY.")
    print("Download file here: https://sites.google.com/a/chromium.org/chromedriver/downloads")
else:
    # Build the connection and cursor
    cnx = mysql.connector.connect(
        user='smartdeckadmin',
        password='UNCCSmartDeck19',
        host='trafficdata.cptl6okwhc5x.us-east-1.rds.amazonaws.com',
        database='trafficlog'
    )
    cursor = cnx.cursor()

    # Get today's date
    tz = pytz.timezone('US/Eastern')
    right_now = datetime.now(tz)
    right_now = right_now.strftime('%Y-%m-%d %H:%M:%S')
    print("1: " + str(right_now))

    # Build query
    add_entry = (
        "INSERT INTO trafficlog.availability ""(time, cone_faculty, cone_visitor, cri, east_1, "
        "east_23, north, sovi, union_lower, union_upper, west) "
        "VALUES ("
        "%(dt)s, "
        "%(d_1)s, "
        "%(d_2)s, "
        "%(d_3)s,"
        "%(d_4)s,"
        "%(d_5)s,"
        "%(d_6)s,"
        "%(d_7)s,"
        "%(d_8)s,"
        "%(d_9)s,"
        "%(d_10)s)")

    deck_availabilities = {}

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--disable-gpu')
    print("2: Arguments set - HEADLESS MODE")

    browser = webdriver.Chrome(chromedriverpath, chrome_options=options)
    browser.get(parking_site)

    print("3: browser launched")
    decks = browser.find_elements_by_class_name("deck-name")
    percents = browser.find_elements(By.XPATH, "//div[contains(@class, 'green') or "
                                               "contains(@class, 'yellow') or "
                                               "contains(@class, 'red') and "
                                               "contains(@class, 'ng-star-inserted')"
                                               "]")
    print("4: Site scrapped")
    for x in range(0, len(decks)):
        deck_availabilities[str(decks[x].get_attribute("innerHTML"))] = \
            str(percents[x].get_attribute("innerHTML")).replace("\n", "")

    d_a = {'dt': right_now, 'd_1': deck_availabilities['Cone Deck Faculty/Staff'],
           'd_2': deck_availabilities['Cone Deck Visitor'], 'd_3': deck_availabilities['CRI Deck'],
           'd_4': deck_availabilities['East Deck 1'], 'd_5': deck_availabilities['East Deck 2/3'],
           'd_6': deck_availabilities['North Deck'], 'd_7': deck_availabilities['South Village Deck'],
           'd_8': deck_availabilities['Union Deck Lower'], 'd_9': deck_availabilities['Union Deck Upper'],
           'd_10': deck_availabilities['West Deck']}

    print("5: Query compiled")

    cursor.execute(add_entry, d_a)
    cnx.commit()
    print("Successfully committed query at " + str(right_now))
    cursor.close()
    cnx.close()
