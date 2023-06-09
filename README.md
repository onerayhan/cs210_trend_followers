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
- Has an Accuracy rate > 0.90
- [Trained Model Link](https://drive.google.com/drive/folders/1sn4JtCZ44wH2FO60Opm3FKXQwYLMtwGY?usp=sharing)  
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

# Quick File Explanations
