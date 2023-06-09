import os, sys, glob, re
import json

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep

from config import LINK_LIST_PATH, LINK_LIST_PATH_GARAN
# Encoding for writing the URLs to the .txt file
# Do not change unless you are getting a UnicodeEncodeError
ENCODING = "utf-8"


def save_link(url, page, path):
    """
    Save collected link/url and page to the .txt file in LINK_LIST_PATH
    """
    id_str = uuid.uuid3(uuid.NAMESPACE_URL, url).hex
    with open(path, "a", encoding=ENCODING) as f:
        f.write("\t".join([id_str, url, str(page)]) + "\n")


def download_links_from_yk_index():
    """
    This function should go to the defined "url" and download the news page links from all
    pages and save them into a .txt file.
    """

    # Checking if the link_list.txt file exists
    if not os.path.exists(LINK_LIST_PATH):
        with open(LINK_LIST_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["id", "url", "page"]) + "\n")
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


    # Start downloading from the page "start_page"
    # which is the page you ended at the last
    # time you ran the code (if you had an error and the code stopped)
    # Create a new instance of the chrome driver
    driver = webdriver.Chrome()
    # Go to your page url
    driver.get('https://www.yapikredi.com.tr/yapi-kredi-hakkinda/piyasa-bulteni/')  # replace with your page url

    wait = WebDriverWait(driver, 10)

    date_input_from = driver.find_element(By.ID, 'txtMarketReleaseDateFrom')
    date_input_from.clear()  # clear any existing date in the input
    date_input_from.send_keys('01.01.2021')  # replace with the date you want

    date_input_to = driver.find_element(By.ID, 'txtMarketReleaseDateTo')
    date_input_to.clear()  # clear any existing date in the input
    date_input_to.send_keys('01.05.2023')  # replace with the date you want
    # locate the button and click it
    retrieve_button = driver.find_element(By.ID, 'btnSearchMarketRelease')
    retrieve_button.click()
    sleep(5)
    while True:
        # Find all the links in the table rows
        links = driver.find_elements(By.CSS_SELECTOR, '#marketReleaseResultContent tr td.lastTd a')
        pages = driver.find_elements(By.CSS_SELECTOR, '#marketReleaseResultContent tr td.firstTd')
        zipped = zip(links, pages)
        for link, page_to_save in zipped:
            collected_url = link.get_attribute('href')
            page = page_to_save.text
            # The following code block saves the collected url and page
            # Save the collected urls one by one so that if an error occurs
            # you do not have to start all over again
            if collected_url not in downloaded_url_list:
                print("\t", collected_url, flush=True)
                save_link(collected_url, page, LINK_LIST_PATH)
            print(link.get_attribute('href'))

        # Try to find the pager-next element to go to the next page
        try:
            next_page_li = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.pager-next')))
            next_page_li.click()
            sleep(2)  # wait for the page to load
        except Exception as e:
            print(e)
            break  # no more pages

    driver.quit()
    #########################################

def download_links_from_garan_index():
    """
    This function should go to the defined "url" and download the news page links from all
    pages and save them into a .txt file.
    """

    # Checking if the link_list.txt file exists
    if not os.path.exists(LINK_LIST_PATH_GARAN):
        with open(LINK_LIST_PATH_GARAN, "w", encoding=ENCODING) as f:
            f.write("\t".join(["id", "url", "page"]) + "\n")
        start_page = 1
        downloaded_url_list = []

    # If some links have already been downloaded,
    # get the downloaded links and start page
    else:
        # Get the page to start from
        data = pd.read_csv(LINK_LIST_PATH_GARAN, sep="\t")
        if data.shape[0] == 0:
            start_page = 1
            downloaded_url_list = []
        else:
            start_page = data["page"].astype("int").max()
            downloaded_url_list = data["url"].to_list()

    # Start downloading from the page "start_page"
    # which is the page you ended at the last
    # time you ran the code (if you had an error and the code stopped)
    # Create a new instance of the chrome driver
    driver = webdriver.Chrome()

    driver.get('https://www.garantibbvayatirim.com.tr/arastirma-raporlari')  # replace with your page url

    wait = WebDriverWait(driver, 10)

    ## sleep is invoked here in order to customly select the date
    sleep(20)
    print("ok")
    # locate the button and click it
    # retrieve_daily_news_button = driver.find_element(By.ID, '11162')
    # retrieve_daily_news_button.click()
    #sleep(5)
    while True:
        # Find all the links in the table rows
        links = driver.find_elements(By.CSS_SELECTOR, 'a.report-download.d-flex')
        dates = driver.find_elements(By.CSS_SELECTOR, 'span.research-publish-date.gtag-date')
        zipped = zip(links, dates)
        page = 0

        for link, date in zipped:
            collected_url = link.get_attribute('href')
            date = date.text[0:10]
            # The following code block saves the collected url and page
            # Save the collected urls one by one so that if an error occurs
            # you do not have to start all over again
            if collected_url not in downloaded_url_list:
                print("\t", collected_url, flush=True)
                save_link(collected_url, date, LINK_LIST_PATH_GARAN)
            #print(link.get_attribute('href'))

        # Try to find the pager-next element to go to the next page
        # keeps clicking the final page when come to the end
        try:
            next_page_li = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.next')))
            next_page_li.click()
            page = page + 1
            sleep(2)  # wait for the page to load
        except Exception as e:
            print(e)
            break  # no more pages

    driver.quit()
    #########################################

def tryout():
    driver = webdriver.Chrome()

    driver.get('https://www.garantibbvayatirim.com.tr/arastirma-raporlari')

    wait = WebDriverWait(driver, 10)
    elements = driver.find_elements(By.CSS_SELECTOR, 'a.report-download.d-flex')
    for element in elements:
        download_link = element.get_attribute('href')
        print(download_link)

if __name__ == "__main__":
    # tryout()
    download_links_from_garan_index()
