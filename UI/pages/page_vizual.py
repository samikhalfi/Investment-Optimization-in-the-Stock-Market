import streamlit as st
import streamlit_shadcn_ui as ui
import requests
import pandas as pd
import json
import re
from utils.nltk_sentiment_analysis import *
from UI.pages.chatbot_page import chatbot_page
from statsmodels.tsa.arima.model import ARIMA
from wordcloud import WordCloud


def display_stock_dashboard():


    with open('json/companies.json') as f:
        companies = json.load(f)

    st.title("Stock Market Investment Dashboard")
  # Toggle the button state

    # Update `use_lemmatization` variable based on the button state
    use_lemmatization = st.session_state.is_button_on

    # Streamlit App Title



    if 'selected_security' in st.session_state:
        company_name = st.session_state['selected_security']
        st.write(f"Selected company: {company_name}")
        # Convert to lowercase for JSON lookup
        company_name_lower = company_name.lower()
        symbol = companies.get(company_name_lower)
        
        if symbol:
            df_historical = pd.read_csv('Data/historical_data.csv')
            from_date = df_historical['Date'].min()
            to_date = df_historical['Date'].max()

            news_df = fetch_company_news(symbol, from_date, to_date)

            if news_df is not None:
                processed_news = analyze_company_news(news_df)

                ui.tabs(options=['Data', 'Graphs', 'Predictions','Chatbot'], default_value='Data', key="main_tabs")

                if st.session_state.main_tabs == 'Data':
                    st.subheader("Processed Company News")

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

                    processed_news['date'] = processed_news['date'].astype(str)
                    with ui.element("div", className="table-container", key="news_table_container"):
                        ui.table(data=processed_news[['headline', 'date', 'processed_headline','sentiment_label']], maxHeight=400, key="news_data_table")

                elif st.session_state.main_tabs == 'Graphs':
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

                    st.subheader("Sentiment Distribution")
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

                    st.subheader("Word Cloud of Headlines")
                    all_words = ' '.join(processed_news['headline'])
                    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_words)

                    st.image(wordcloud.to_array())

                elif st.session_state.main_tabs == 'Predictions':
                    st.subheader("Stock Price Forecast")
                    df_historical['Date'] = pd.to_datetime(df_historical['Date'])
                    df_historical.set_index('Date', inplace=True)

                    model = ARIMA(df_historical['Close'], order=(1, 1, 1))
                    model_fit = model.fit()
                    forecast = model_fit.forecast(steps=3)

                    forecast_dates = pd.date_range(start=pd.to_datetime('now'), periods=3)
                    predicted_prices = forecast.values

                    st.subheader("Predicted Prices for the Next 3 Days:")
                    cols = st.columns(3)
                    with cols[0]:
                        ui.card(title=f"Price predicted for {forecast_dates[0].date()}", content=f"{predicted_prices[0]:.2f}", description="", key="forecast1").render()
                    with cols[1]:
                        ui.card(title=f"Price predicted for {forecast_dates[1].date()}", content=f"{predicted_prices[1]:.2f}", description="", key="forecast2").render()
                    with cols[2]:
                        ui.card(title=f"Price predicted for {forecast_dates[2].date()}", content=f"{predicted_prices[2]:.2f}", description="", key="forecast3").render()

                    forecast_df = pd.DataFrame({
                        'Date': forecast_dates,
                        'Predicted Close Price': predicted_prices
                    })

                    combined_df = df_historical[['Close']].copy()
                    combined_df = pd.concat([combined_df, forecast_df.set_index('Date')])

                    st.line_chart(combined_df)
                elif st.session_state.main_tabs == 'Chatbot' :
                    chatbot_page() 


        else:
            st.error("Company not found in the JSON file.")