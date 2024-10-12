import pandas as pd
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
import re

# Load the CSV file
data = pd.read_csv("News_Titles.csv")

# Keep only the 'headline' column
data_headline_only = data[['headline']]

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Define a custom list of stop words (add or remove as needed)
custom_stop_words = set(stopwords.words('english'))
# You can add important words to retain
additional_stop_words = {'not', 'should', 'has', 'to', 'this', 'still'}
custom_stop_words = custom_stop_words - additional_stop_words

# Initialize the Sentiment Intensity Analyzer
sia = SentimentIntensityAnalyzer()

# Function to preprocess text
def preprocess_text(text):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Use regex to preserve specific terms (e.g., company names, ticker symbols)
    text = re.sub(r'\b(Apple Inc|AVUS|AAPL)\b', lambda x: x.group(0).lower(), text)
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Remove stop words and perform lemmatization
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.lower() not in custom_stop_words]
    
    # Join the tokens back into a single string
    return ' '.join(tokens)

# Apply preprocessing to the headlines
data_headline_only['processed_headline'] = data_headline_only['headline'].apply(preprocess_text)

# Function to calculate sentiment score
def get_sentiment_score(text):
    return sia.polarity_scores(text)['compound']

# Apply sentiment analysis to the processed headlines
data_headline_only['sentiment_score'] = data_headline_only['processed_headline'].apply(get_sentiment_score)

# Print all the processed headlines and sentiment scores
pd.set_option('display.max_rows', None)  # Ensure all rows are printed
pd.set_option('display.max_columns', None)  # Ensure all columns are printed
print(data_headline_only)
