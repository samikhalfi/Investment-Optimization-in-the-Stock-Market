import pandas as pd
import json
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer



def load_important_words(file_path):
    with open(file_path) as f:
        important_words = json.load(f)
    all_important_words = set()
    for category in important_words.values():
        all_important_words.update(category)
    return all_important_words

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
    sentiment_labels = []
    sentiment_scores = []
    for score in scores:
        sentiment_scores.append(score)
        if score > 0.05:
            sentiment_labels.append('Positive')
        elif score < -0.05:
            sentiment_labels.append('Negative')
        else:
            sentiment_labels.append('Neutral')

    return pd.Series(sentiment_scores), pd.Series(sentiment_labels)

def calculate_relevance_score(headlines, important_words):
    relevance_scores = []
    for headline in headlines:
        words = set(headline.lower().split())
        relevance_score = sum(1 for word in words if word in important_words)
        relevance_scores.append(relevance_score)
    return pd.Series(relevance_scores)

def analyze_company_news(data_path, important_words_path, output_path, use_lemmatization=True):
    data = pd.read_csv(data_path)
    important_words = load_important_words(important_words_path)
    data_headline_only = data[['headline']].copy()
    data_headline_only['relevance_score'] = calculate_relevance_score(data_headline_only['headline'], important_words)
    data_headline_only['sentiment_score'], data_headline_only['sentiment_label'] = get_sentiment_nltk(data_headline_only['headline'], use_lemmatization)
    
    output_df = data_headline_only[['headline', 'relevance_score', 'sentiment_score', 'sentiment_label']]
    output_df.to_csv(output_path, index=False)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None) 
    print(output_df)

if __name__ == "__main__":
    data_path = "Data/Company_News.csv"
    important_words_path = 'json/important_words.json'
    output_path = "Data/Processed_Company_News.csv"
    
    analyze_company_news(data_path, important_words_path, output_path)
    