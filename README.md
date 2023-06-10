# Financial Sentiment Analysis with BERT for Borsa Istanbul (BIST100)

- Hello, This is the repository for our Project for cs210 in which we've trained a Financial Sentiment Analysis model using Bert for Borsa Istanbul. Knowing live alternatives cost more than 750 TL for a month this project will be further upgraded as a live open-source alternative to its rivals. Please Star the project for further upgrades :))   

- Here you can find the code of the data gathering, parsing, model training and visualizations in different folders.
All the documentation is public and open-source.
This sheet will be updated, but for the moment
let's get a good grade :)

-----------------------------------------------

# Links to resources
- Here data and trained model's source is shared through google drive since they are significantly big in size or quantity
------------------------------------------------------------ 
## Link to the Trained Model
- Trained Model can be directly downloaded and tuned for live sentiment analysis.
- Has an Accuracy rate > 0.90 for the test data 
- [Trained Model Link](https://huggingface.co/onerayhan/bert_finance_BIST100)  
------------------------------------------------------------
## Link to the Prelabeled Data
- Data is prelabeled with Daily Return Value of the Bist-100 in order to get a first insight
- They can be found as classified neg-pos subfolders
- [Pre-Labeled Data Link](https://drive.google.com/drive/folders/1NYB9wBx8yt31drdczAB_ll5s31I1dcN4?usp=sharing)  
-------------------------------------------------------------
## Link to the True Labeled Data 
- Data then labeled another time with keyword searching and more than 200 files have changed directory from neg to pos or vice-versa: 
- [Labeled Data Link](https://drive.google.com/drive/folders/1sn4JtCZ44wH2FO60Opm3FKXQwYLMtwGY?usp=sharing)

# Additional Notes

## Data Gathering
- We've gathered Daily Brokerage Reviews, Daily News and Tweets for the training but haven't used the tweets data in the training part of the model because of its limitations and high spam percentage
- We've set the starting period as 01.01.21 and ending time as 25.05.23 except for tweets which we couldn't access earlier than 1 month
- We've gathered the data through various libraries such as Selenium, Requests, BeautifulSoup and SnScrape  
## Data Preprocessing
- We've used built-in python libraries, pypdfium, Pandas, Numpy, Transformers and BertTokenizer for preprocessing
## Model Training 
- We've used a Turkish Cased Bert for training the data with Transformers
- [Link to Untrained Model](https://huggingface.co/dbmdz/bert-base-turkish-cased)
## Visualization
- We've Used Matplotlib and Seaborn for visualizations
 
-----------------------------------------------

# Quick File Explanations
Below are quick explanation about what every code does, 
the workings of the python code could be understood more by looking at the comments in each code.

## Downloading Links

- akbank_link_download.py

  Downloads links to PDFs in the specified url until 04.01.2021 using selenium to traverse interactive page in akbank website

- gedik_link_download.py

  Downloads links to PDFs in the specified url using requests and BeautifulSoup to sequentially take links from gedik website
  
- download_links_yk_garan
  Downloads links to PDFs in the specified url using requests, BeautifulSoup and Selenium to sequentially take links from Garanti and YapıKredi website

## Downloading PDFs

- akbank_PDF_download.py

  Gets .txt file of links and downloads PDFs from it and saves them to /data/akbank_PDF, folders need to be created beforehand

- garanti_PDF_download.py

  Gets .txt file of links and downloads PDFs from it and saves them to /data/garanti_PDF, folders need to be created beforehand


- gedik_PDF_download.py

  Gets .txt file of links and downloads PDFs from it and saves them to /data/gedik_PDF, folders need to be created beforehand


- yapikredi_PDF_download.py

  Gets .txt file of links and downloads PDFs from it and saves them to /data/yapikredi_PDF, folders need to be created beforehand

## Extracting Text

- pypdfium2_akbank.py

  Using pypdfium2 to get necessary text from gedik pdfs located in data/yapikredi_PDF
  put all extracted text into a list of dictionaries where date, count, paragraph are keys
  put the combined dictionaries into .json file


- pypdfium2_garanti.py

  Using pypdfium2 to get necessary text from garanti pdfs located in data/garanti_PDF
  put all extracted text into a list of dictionaries where date, count, paragraph are keys
  put the combined dictionaries into .json file


- pypdfium2_gedik.py

  Using pypdfium2 to get necessary text from gedik pdfs located in data/gedik_PDF
  put all extracted text into a list of dictionaries where date, monthAgo, count, paragraph are keys
  put the combined dictionaries into .json file


- pypdfium2_yapikredi.py

  Using pypdfium2 to get necessary text from gedik pdfs located in data/yapikredi_PDF
  put all extracted text into a list of dictionaries where date, count, paragraph are keys
  put the combined dictionaries into .json file

## .Json Labeling

After text extraction the output .json files were processed by dividing them by BIST-100 values such that,
if a text was published while BIST-100 had a negative change the processed text was put into the negative folder
else it was put into the positive folder, these folders would serve as the labeled data for our machine learning model

- json_sorter.py

  In this program received data is a json file containing list of dictionary with keys date, count, and paragraph.
  The date of each element will be compared with XU100 excel sheet where changes in BIST-100 value are located.
  The dates of dictionaries will be found in XU100 and will be sorted into negative folder if value is negative 
  or into positive folder if value is positive.


- json_sort_haberler.py

  In this program received data is a json file containing list of dictionary with keys date, count, and paragraph.
  The date of each element will be compared with XU100 excel sheet where changes in BIST-100 value are located.
  The dates of dictionaries will be found in XU100 and will be sorted into negative folder if value is negative 
  or into positive folder if value is positive.


- json_sort_tweet.py

  In this program received data is a json file containing dictionary of dictionary with id as keys and 
  date, tweet, views as values. The date of each element will be compared with XU100 excel sheet where 
  changes in BIST-100 value are located. The dates of dictionaries will be found in XU100 and will be 
  sorted into negative folder if value is negative or into positive folder if value is positive.
## True Labeling

- parse_keywords.py
  checks each neg or pos assigned files keywords and move them to other folder if falsely labeled
  
## Model Training

- bert_train
  + Trains the data with Bert Model and checks the results. Bert Tokenizer is also used to further preprocess the data.
  + To see the results and scores of the model please check this file.
  
## Visualizations 

- Visualizations.ipynb
  To show the performance on of the model on whole data and to visualize the sentiments made from brokerages or news this file is implemented.
- CS210Visualization.pptx 
- sentiment_of_broker_sites.ipynb
  Plots the sentiment of 4 different broker sites as percentage comparisons with positive and negative sentiments as categories
