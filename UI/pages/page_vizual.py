import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
import json
from statsmodels.tsa.arima.model import ARIMA
from wordcloud import WordCloud
from UI.pages.chatbot_page import chatbot_page
from utils.nltk_sentiment_analysis import *

def display_stock_dashboard():
    # Load company data from JSON
    with open('json/companies.json') as f:
        companies = json.load(f)
    
    # Title with styling
    st.markdown("<h1 style='text-align: center; color: #fe735d;'>📈 Stock Market Investment Dashboard 📉</h1>", unsafe_allow_html=True)
    st.divider()

    # Check if a company is selected in session state
    if 'selected_security' in st.session_state:
        company_name = st.session_state['selected_security']
        st.subheader(f"Selected Company: **{company_name}**")
        st.divider()

        # Convert company name to lowercase for JSON lookup
        company_name_lower = company_name.lower()
        symbol = companies.get(company_name_lower)
        
        if symbol:
            # Load historical data and get date range
            df_historical = pd.read_csv('Data/historical_data.csv')
            from_date = df_historical['Date'].min()
            to_date = df_historical['Date'].max()

            # Fetch and process company news
            news_df = fetch_company_news(symbol, from_date, to_date)
            if news_df is not None:
                # Set up tabs with "Data" as the default selected
                selected_tab = ui.tabs(options=['Data', 'Graphs', 'Predictions', 'Chatbot'], default_value='Data', key="main_tabs")
                
                # Processed company news
                processed_news = analyze_company_news(news_df)

                # Display Data Tab (default)
                st.subheader("Processed Company News")
                st.divider()
                
                cols = st.columns(3)
                with cols[0]:
                    total_news_count = len(processed_news)
                    ui.card(title="Total Headlines", content=str(total_news_count), description="Total news articles fetched", key="total_news_card").render()
                with cols[1]:
                    latest_date = processed_news['date'].max()
                    ui.card(title="Latest News Date", content=str(latest_date), description="Most recent news article date", key="latest_date_card").render()
                with cols[2]:
                    most_common_sentiment = processed_news['sentiment_label'].mode()[0]
                    ui.card(title="Most Common Sentiment", content=most_common_sentiment, description="Dominant sentiment across news", key="common_sentiment_card").render()
                
                # Show processed news table
                processed_news['date'] = processed_news['date'].astype(str)
                st.divider()
                st.table(processed_news[['headline', 'date', 'processed_headline', 'sentiment_label']])

                # Display the selected tab contents
                if selected_tab == 'Graphs':
                    st.divider()
                    st.subheader("Sentiment Analysis")
                    
                    cols = st.columns(3)
                    with cols[0]:
                        positive_count = processed_news['sentiment_label'].value_counts().get('Positive', 0)
                        ui.card(title="Positive Sentiment", content=str(positive_count), description="Number of positive headlines", key="positive_card").render()
                    with cols[1]:
                        negative_count = processed_news['sentiment_label'].value_counts().get('Negative', 0)
                        ui.card(title="Negative Sentiment", content=str(negative_count), description="Number of negative headlines", key="negative_card").render()
                    with cols[2]:
                        neutral_count = processed_news['sentiment_label'].value_counts().get('Neutral', 0)
                        ui.card(title="Neutral Sentiment", content=str(neutral_count), description="Number of neutral headlines", key="neutral_card").render()
                    
                    # Sentiment Distribution Bar Chart
                    sentiment_counts = processed_news['sentiment_label'].value_counts()
                    sentiment_df = pd.DataFrame({
                        'Sentiment': sentiment_counts.index,
                        'Count': sentiment_counts.values
                    })
                    st.vega_lite_chart(sentiment_df, {
                        'mark': {'type': 'bar', 'tooltip': True},
                        'encoding': {
                            'x': {'field': 'Sentiment', 'type': 'ordinal'},
                            'y': {'field': 'Count', 'type': 'quantitative', 'axis': {'grid': False}},
                        },
                    }, use_container_width=True)
                    
                    # Word Cloud of Headlines
                    st.subheader("Word Cloud of Headlines")
                    all_words = ' '.join(processed_news['headline'])
                    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_words)
                    st.image(wordcloud.to_array())
                    
                elif selected_tab == 'Predictions':
                    st.divider()
                    st.subheader("Stock Price Forecast")
                    
                    df_historical['Date'] = pd.to_datetime(df_historical['Date'])
                    df_historical.set_index('Date', inplace=True)
                    
                    model = ARIMA(df_historical['Close'], order=(1, 1, 1))
                    model_fit = model.fit()
                    forecast = model_fit.forecast(steps=3)
                    
                    forecast_dates = pd.date_range(start=pd.to_datetime('now'), periods=3)
                    predicted_prices = forecast.values
                    
                    cols = st.columns(3)
                    for i, price in enumerate(predicted_prices):
                        ui.card(title=f"Price for {forecast_dates[i].date()}", content=f"{price:.2f}", key=f"forecast_{i+1}").render()
                    
                    # Forecast Line Chart
                    forecast_df = pd.DataFrame({'Date': forecast_dates, 'Predicted Close Price': predicted_prices})
                    combined_df = pd.concat([df_historical[['Close']], forecast_df.set_index('Date')])
                    st.line_chart(combined_df)
                    
                elif selected_tab == 'Chatbot':
                    st.divider()
                    chatbot_page()
        else:
            st.error("Company not found in the JSON file.")

