# coding=UTF-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time


import pandas as pd
import os

"""
    downloads links to PDFs in the specified url until 04.01.2021 using selenium to traverse interactive page
"""

ENCODING = "utf-8"

LINK_LIST_PATH = "data/link_list.txt"
URL_PATH = "https://yatirim.akbank.com/tr-tr/raporlar/Sayfalar/Raporlar.aspx"


"""
!!! save_link(), download_links_from_index() taken from cs210 HW2 download_links.py !!!
"""


def save_link(url, date, page):
    """
    Save collected link/url and page to the .txt file in LINK_LIST_PATH
    """
    with open(LINK_LIST_PATH, "a", encoding=ENCODING) as f:
        f.write("\t".join([url, date, str(page)]) + "\n")


def download_links_from_index():
    """
    This function should go to the defined "url" and download the news page links from all
    pages and save them into a .txt file.
    """

    # Checking if the link_list.txt file exists
    if not os.path.exists(LINK_LIST_PATH):
        with open(LINK_LIST_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["url", "datetime", "page"]) + "\n")
        start_page = 1
        downloaded_url_list = []

    # If some links have already been downloaded,
    # get the downloaded links and start page
    else:
        # Get the page to start from
        data = pd.read_csv(LINK_LIST_PATH, sep="\t")
        if data.shape[0] == 0:
            start_page = 1
            downloaded_url_list = []
        else:
            start_page = data["page"].astype("int").max()
            downloaded_url_list = data["url"].to_list()

    return downloaded_url_list


# keeps pressing the button located at the bottom of the page,
# provides new daily report links to download


def keep_pressing_button():
    while True:
        try:
            # wait for the "DAHA FAZLA" button to be clickable
            print("clicking DAHA FAZLA...")
            button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn more-btn']")))
            # Check the display style of the button
            if driver.execute_script("return window.getComputedStyle(arguments[0]).display;", button) == 'none':
                break

            # click "DAHA FAZLA" button
            button.click()

            # delay for loading the new items
            time.sleep(5)
        except:
            # no more "DAHA FAZLA" buttons, or other error occurred.
            break


# presses the button to download links to PDFs
# presses for each available button
# also gets date information located near button


def get_url_and_date():

    # Now, all items should be loaded, and you can scrape the buttons
    buttons = driver.find_elements(By.XPATH, "//a[@class='download-report-btn']")
    dates   = driver.find_elements(By.XPATH, "//span[@class='date']")

    # Extract date, url attributes from button elements
    links    = [button.get_attribute('href') for button in buttons]
    datet = [date.get_attribute("innerText") for date in dates]

    return links, datet


# changes the interactive calendar near the submit button
# changes calendar range 1 month back


def change_month():

    # find startDate bar and click into it
    date_start = driver.find_element(By.XPATH, "//input[@id='startDate']")
    date_start.click()

    # click previous month arrow to go back 1 month
    prev = driver.find_element(By.XPATH, "//th[@class='prev']")
    prev.click()

    # click the 1st day of the month
    calender_start = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//td[@class='day' and contains(text(), '1')]")))
    calender_start.click()

    # find and click into endDate bar
    date_end = driver.find_element(By.XPATH, "//input[@id='endDate']")
    date_end.click()

    # click 28th if it is february, otherwise select 30th day
    if driver.find_element(By.XPATH, "//th[@class='datepicker-switch']").get_attribute("innerText").find("Şubat") != -1:
        calender_end = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//td[@class='day' and contains(text(), '28')]")))
    else:
        calender_end = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//td[@class='day' and contains(text(), '30')]")))

    calender_end.click()


def get_monthly_links(final_date):

    reached_date = False

    # presses "DAHA FAZLA" until it cant
    keep_pressing_button()
    print("end of month")

    # the url list dates that will be saved into the .txt file
    real_url_dates = []

    urls, url_dates = get_url_and_date()

    for url_date in url_dates:

        # using "0X.0X.20XX" format for dates
        url_date = ".".join([x.zfill(2) for x in url_date.split(".")])
        real_url_dates.append(url_date)
        # print(url_date)

        if url_date == final_date:
            reached_date = True

    if not reached_date:
        for collected_url, real_url_date in zip(urls, real_url_dates):

            if collected_url not in downloaded_url_list:
                print("\t", collected_url, flush=True)
                save_link(collected_url, real_url_date, page)

    # go back 1 month
    change_month()

    # confirm date change and press submit to open new page with more links
    submit.click()

    return reached_date


# need to click into calendar and set dates to cycle through


def special_begin():

    date_start = driver.find_element(By.XPATH, "//input[@id='startDate']")
    date_end = driver.find_element(By.XPATH, "//input[@id='endDate']")

    # !for calendar to pop up need to click into empty bar!
    date_start.click()

    # set beginning day the 1st of current month
    calender_start = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//td[contains(text(), '1')]")))

    calender_start.click()

    # !for calendar to pop up need to click into empty bar!
    date_end.click()

    # set end date today
    calender_today = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//td[@class='today day']")))

    # !for calendar to pop up need to click into empty bar!
    calender_today.click()


# #-----------------------------------<beginning>-----------------------------------#

# create link list if not available
downloaded_url_list = download_links_from_index()

# Setup WebDriver
driver = webdriver.Chrome()
driver.get(URL_PATH)

# "Uygula" button setup
select = Select(driver.find_element(By.XPATH, "//select[@class='select2-hidden-accessible']"))
select.select_by_visible_text('Akbank Günlük Bülten')
submit = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn red-btn submit-btn']")))

# beginning special case setup
special_begin()

# click "Uygula"
submit.click()

# end signal
terminate = False

# gets months worth of links
# ends when reached date in the parameter of get_monthly_links

page = 0
while not terminate:
    page = page+1
    if get_monthly_links("04.01.2021"):
        terminate = True

# Close the WebDriver
driver.quit()
