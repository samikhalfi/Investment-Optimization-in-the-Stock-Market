import pandas as pd
import json
import re
import nltk
import requests
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import streamlit as st

API_KEY = 'your_api_key'

def fetch_company_news(symbol, from_date, to_date):
    url = f'https://finnhub.io/api/v1/company-news?symbol={symbol}&from={from_date}&to={to_date}&token={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()
        news_df = pd.DataFrame(news_data)
        if 'datetime' in news_df.columns:
            news_df['date'] = pd.to_datetime(news_df['datetime'], unit='s').dt.date
        return news_df[['headline', 'date', 'url']]
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def preprocess_text_nltk(text, use_lemmatization=True):
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    if use_lemmatization:
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
    else:
        tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join(tokens)

def get_sentiment_nltk(processed_headlines, use_lemmatization=True):
    sia = SentimentIntensityAnalyzer()
    processed_headlines = processed_headlines.apply(lambda x: preprocess_text_nltk(x, use_lemmatization))
    scores = processed_headlines.apply(lambda x: sia.polarity_scores(x)['compound'])
    sentiment_labels = ['Positive' if score > 0.05 else 'Negative' if score < -0.05 else 'Neutral' for score in scores]
    return pd.Series(scores), pd.Series(sentiment_labels)

def analyze_company_news(news_df):
    # Add a radio button for lemmatization vs. stemming choice within the function
    choice = st.radio("Select Text Processing Method", ("Lemmatization", "Stemming"))
    use_lemmatization = True if choice == "Lemmatization" else False

    # Process the headlines and add them to the DataFrame
    news_df['processed_headline'] = news_df['headline'].apply(lambda x: preprocess_text_nltk(x, use_lemmatization))
    
    # Format the processed headlines to be bold for markdown rendering
    news_df['processed_headline'] = '**' + news_df['processed_headline'] + '**'

    important_words = load_important_words(r'json\important_words.json')
    news_df['relevance_score'] = calculate_relevance_score(news_df['headline'], important_words)
    news_df['sentiment_score'], news_df['sentiment_label'] = get_sentiment_nltk(news_df['processed_headline'], use_lemmatization)


    # Save the DataFrame with processed headlines to a CSV file
    news_df.to_csv('data/processed_company_news.csv', index=False)
    
    return news_df




def load_important_words(file_path):
    with open(file_path) as f:
        important_words = json.load(f)
    return {word for category in important_words.values() for word in category}

def calculate_relevance_score(headlines, important_words):
    return pd.Series([sum(1 for word in headline.lower().split() if word in important_words) for headline in headlines])

