import streamlit as st
import requests
import pandas as pd
import json
import yfinance as yf
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from statsmodels.tsa.arima.model import ARIMA
import os

# Initialize NLTK resources
nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('wordnet')

# API Key
API_KEY = 'cs4p4u1r01qgd1p6742gcs4p4u1r01qgd1p67430'

# Load company names and symbols
with open(r'C:\Users\anask\Desktop\Investment-Optimization-in-the-Stock-Market-main\Data\companies.json', 'r') as f:
    companies = json.load(f)

# Function to fetch company news
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

# NLTK text processing functions
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
    important_words = load_important_words(r'C:\Users\anask\Desktop\Investment-Optimization-in-the-Stock-Market-main\json\important_words.json')
    news_df['relevance_score'] = calculate_relevance_score(news_df['headline'], important_words)
    news_df['sentiment_score'], news_df['sentiment_label'] = get_sentiment_nltk(news_df['headline'])
    return news_df

def load_important_words(file_path):
    with open(file_path) as f:
        important_words = json.load(f)
    return {word for category in important_words.values() for word in category}

def calculate_relevance_score(headlines, important_words):
    return pd.Series([sum(1 for word in headline.lower().split() if word in important_words) for headline in headlines])

# Streamlit App
st.title("Stock Market Investment Dashboard")

# User input for company name
company_name = st.text_input("Enter the company name:")

if company_name:
    company_name_lower = company_name.lower()
    symbol = companies.get(company_name_lower)
    
    if symbol:
        # Load historical data
        df_historical = pd.read_csv(r'C:\Users\anask\Desktop\Investment-Optimization-in-the-Stock-Market-main\Data\historical_data.csv')
        from_date = df_historical['Date'].min()
        to_date = df_historical['Date'].max()

        # Fetch company news
        news_df = fetch_company_news(symbol, from_date, to_date)

        if news_df is not None:
            # Analyze news
            processed_news = analyze_company_news(news_df)

            # Display Processed News Data
            st.write("Processed News Data:")
            st.dataframe(processed_news)

            # Sentiment Distribution
            st.subheader("Sentiment Distribution")
            sentiment_counts = processed_news['sentiment_label'].value_counts()
            sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette='viridis')
            plt.title('Sentiment Distribution')
            plt.xlabel('Sentiment')
            plt.ylabel('Count')
            st.pyplot(plt)

            # Word Cloud
            st.subheader("Word Cloud of Headlines")
            all_words = ' '.join(processed_news['headline'])
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_words)
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(plt)

            # Time Series Forecast
            st.subheader("Stock Price Forecast")
            df_historical['Date'] = pd.to_datetime(df_historical['Date'])
            df_historical.set_index('Date', inplace=True)

            model = ARIMA(df_historical['Close'], order=(1, 1, 1))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=3)

            forecast_dates = pd.date_range(start=pd.to_datetime('now'), periods=3)
            predicted_prices = forecast.values

            st.write("Predicted Prices for the Next 3 Days:")
            for date, price in zip(forecast_dates, predicted_prices):
                st.write(f'Price predicted for {date.date()}: {price}')

            # Plot the historical and predicted prices
            plt.figure(figsize=(10, 5))
            plt.plot(df_historical['Close'], label='Actual Prices', marker='o')
            plt.scatter(forecast_dates, predicted_prices, color='green', label='Predicted Prices', marker='x')
            plt.title('Stock Price Forecast')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.axvline(x=pd.to_datetime('now'), color='r', linestyle='--', label='Forecast Start')
            plt.legend()
            st.pyplot(plt)
    else:
        st.error("Company not found in the JSON file.")
