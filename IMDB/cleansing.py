import json
import io
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import re
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# # Load SpaCy model 
# nlp = spacy.load('en_core_web_sm')
# stop_words = nlp.Defaults.stop_words

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# Cleansing part consists of Various steps :

def readDataFromJsonFile():
    try:
        with io.open('data.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data
    except json.decoder.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")

def tokenize_and_remove_stopwords(text):
    words = word_tokenize(text)
    words = [word for word in words if word.lower() not in stop_words]
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(lemmatized_words)

def cleanText(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def cleanseData(rawData):
    for data in rawData:
        reviews = rawData[data]["reviews"]
        print(reviews)
        for review in reviews:
            review = cleanText(review)
            review = tokenize_and_remove_stopwords(review)

        # print(review['reviews'])
        # print(review['details
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

def main():
    
    rawData = readDataFromJsonFile()

    details_list = []
    for key, value in rawData.items():
        details = value["details"]
        details_list.append({
            "Movie Name": details["movie_Name"],
            "Genres": ", ".join(details["genre"]),
            "Other": ", ".join(details["other"]),
            "Review":review
        })

    details_df = pd.DataFrame(details_list)
    # Create DataFrame for reviews
    reviews_list = []
    for key, value in rawData.items():
        for review in value["reviews"]:
            reviews_list.append({
                "Movie Name": value["details"]["movie_Name"],
                "Review": review
            })

    reviews_df = pd.DataFrame(reviews_list)

    # Display the DataFrames
    print("Movie Details:")
    # print(details_df.head())
    print("\nReviews:")
    

    reviews_df["cleansedReview"] = reviews_df["Review"].apply(cleanText)
    reviews_df["tokenized_reviews"] = reviews_df["cleansedReview"].apply(tokenize_and_remove_stopwords)
    reviews_df['sentiment'] = reviews_df['cleansedReview'].apply(get_sentiment)
    # print(reviews_df.head())

    details_df["sentiment"] = reviews_df["sentiment"]

    plt.figure(figsize=(10,6))
    sns.histplot(reviews_df['sentiment'], kde=True)
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment')
    plt.ylabel('Frequency')
    plt.show()

    # print(details_df.head())

    genre_sentiment_data = []

    for index, row in details_df.iterrows():
        genres = row['Genres'].split(', ')
        for genre in genres:
            genre_sentiment_data.append({'Genre': genre, 'Sentiment': row['sentiment']})

    genre_sentiment_df = pd.DataFrame(genre_sentiment_data)

    print(genre_sentiment_df.head())

    # plt.figure(figsize=(14,8))
    # sns.boxplot(x='Genre', y='Sentiment', data=genre_sentiment_df)
    # plt.title('Sentiment Distribution by Genre')
    # plt.xlabel('Genre')
    # plt.ylabel('Sentiment')
    # plt.xticks(rotation=90)
    # plt.show()

    # cleanseData(rawData)
    # for data in rawData:
    #     print(data)


if __name__ == "__main__":
    main()
