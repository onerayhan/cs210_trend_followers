import requests
from bs4 import BeautifulSoup

base_url = "https://bigpara.hurriyet.com.tr/borsa/haber/"
page_count = 40  # Number of pages to scrape

output = []  # List to store the dictionaries for each news article
seen_titles = set()  # Set to track the titles

for page in range(1, page_count + 1):
    url = base_url + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    news_list = soup.find_all("ul")  # Assuming each news article is contained within an <ul> element

    for i, news in enumerate(news_list):
        if i == 0:
            continue  # Skip the first cell

        news_dict = {}  # Dictionary to store the information for each news article

        title_element = news.find("h2", class_="newsTitle1")
        if title_element is not None:
            title = title_element.text.strip()
            if title and not title.isspace() and title not in seen_titles:
                news_dict["Title"] = title.strip()
                seen_titles.add(title)

        date_element = news.find("li", class_="cell012")
        if date_element is not None:
            date = date_element.text.strip()
            if date != "Tarih":
                news_dict["Date"] = date

        time_element = news.find("li", class_="cell024")
        if time_element is not None:
            time = time_element.text.strip()
            if time != "Saat":
                news_dict["Time"] = time

        if "Title" in news_dict and ("Date" in news_dict and "Time" in news_dict):
            output.append(news_dict)

# Save the scraped information as a list of dictionaries
with open("haberler.txt", "w", encoding="utf-8") as file:
    file.write(str(output))

