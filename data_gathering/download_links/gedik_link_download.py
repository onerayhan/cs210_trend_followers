import os
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


"""
    downloads links to PDFs in the specified url using requests and BeautifulSoup to sequentially take links from every page
"""


# Encoding for writing the URLs to the .txt file
# Do not change unless you are getting a UnicodeEncodeError

LINK_LIST_PATH = "data/link_list.txt"

ENCODING = "utf-8"

"""
!!! save_link(), download_links_from_index() taken from cs210 HW2 download_links.py !!!
"""


def save_link(date, url, page):
    """
    Save collected link/url and page to the .txt file in LINK_LIST_PATH
    """
    with open(LINK_LIST_PATH, "a", encoding=ENCODING) as f:
        f.write("\t".join([date, url, str(page)]) + "\n")


def download_links_from_index():
    """
    This function should go to the defined "url" and download the news page links from all
    pages and save them into a .txt file.
    """

    # Checking if the link_list.txt file exists
    if not os.path.exists(LINK_LIST_PATH):
        with open(LINK_LIST_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["date", "url", "page"]) + "\n")
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

    rootURL  = "https://gedik.com/analiz/rapor-ve-analizler/yurt-ici-piyasa-rapor-ve-analizleri?page="
    rootURL2 = '&categoryName=Günlük-Bülten&scrollTo=marketReleases'

    for pid in range(1, 21):

        pageURL = "{}{}{}".format(rootURL, pid, rootURL2)
        print(pageURL)

        resp = requests.get(pageURL)

        soup = bs(resp.text)

        for item in soup.find("div", {"class": "css-1tepnq0"}).find_all("a"):

            collected_date = item.find("div", {"class": "chakra-text richTextClass css-1cy6k6t"}).text[-10:]

            # Save the collected url in the variable "collected_url"
            collected_url = item["href"]

            print(collected_url)

            # Save the page that the url is taken from in the variable "page"
            page = pid

            if collected_url not in downloaded_url_list:
                print("\t", collected_url, flush=True)
                save_link(collected_date, collected_url, page)

    # The following code block saves the collected url and page
    # Save the collected urls one by one so that if an error occurs


if __name__ == "__main__":
    download_links_from_index()


