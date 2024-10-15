import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
import json
from statsmodels.tsa.arima.model import ARIMA
from wordcloud import WordCloud
from UI.pages.chatbot_page import chatbot_page
from utils.nltk_sentiment_analysis import *
import altair as alt
import numpy as np

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

                # Display the selected tab contents
                if selected_tab == 'Data':
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

                elif selected_tab == 'Graphs':
                    st.subheader("Sentiment Analysis")
                    st.divider()
                    
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

                    st.subheader("Stock Dashboard")
                    st.divider()
                    # Créer une colonne pour la mise en page
                    col1, col2 = st.columns(2)  # Créez deux colonnes

                    # **Premier graphique (Word Cloud)**
                    with col1:
                        st.subheader("Word Cloud of Headlines")
                        all_words = ' '.join(processed_news['headline'])
                        wordcloud = WordCloud(width=400, height=200, background_color='white').generate(all_words)
                        st.image(wordcloud.to_array())

                    # **Deuxième graphique (Stock High Prices)**
                    with col2:
                        st.subheader("Stock High Prices Over Time")
                        # Assurez-vous que la colonne 'Date' est au format datetime
                        df_historical['Date'] = pd.to_datetime(df_historical['Date'])
                        line_chart_style = alt.Chart(df_historical).mark_line(point=True).encode(
                            x=alt.X('Date:T', title='Date'),
                            y=alt.Y('High:Q', title='High Price'),
                            tooltip=['Date:T', 'High:Q'],
                            color=alt.value("#fe735d")
                        ).properties(
                            width=400,  # Largeur réduite
                            height=200  # Hauteur réduite
                        ).interactive()

                        st.altair_chart(line_chart_style, use_container_width=True)

                    # Créer une nouvelle rangée pour les deux derniers graphiques
                    col3, col4 = st.columns(2)  # Créez deux colonnes pour la deuxième rangée

                    # **Troisième graphique (Area Chart of Closing Prices)**
                    with col3:
                        st.subheader("Area Chart of Closing Prices")
                        area_chart = alt.Chart(df_historical).mark_area(
                            opacity=0.5,
                            interpolate='basis'
                        ).encode(
                            x=alt.X('Date:T', title='Date'),
                            y=alt.Y('Close:Q', title='Closing Price'),
                            tooltip=['Date:T', 'Close:Q']
                        ).properties(
                            width=400,  # Largeur réduite
                            height=200  # Hauteur réduite
                        ).interactive()

                        st.altair_chart(area_chart, use_container_width=True)

                    # **Quatrième graphique (Répartition des Volumes d'Actions)**
                    with col4:
                        st.subheader("Répartition des Volumes d'Actions")
                        volume_bins = pd.cut(df_historical['Volume'], bins=[0, 1e7, 2e7, 3e7, 4e7, 5e7], right=False)
                        volume_counts = volume_bins.value_counts().reset_index()
                        volume_counts.columns = ['Volume Range', 'Count']
                        volume_counts['Volume Range'] = volume_counts['Volume Range'].apply(lambda x: f"{int(x.left)} - {int(x.right)}")

                        circle_chart_volume = alt.Chart(volume_counts).mark_arc(innerRadius=50).encode(
                            theta=alt.Theta(field='Count', type='quantitative'),
                            color=alt.Color(field='Volume Range', type='nominal'),
                            tooltip=['Volume Range', 'Count']
                        ).properties(
                            title="Répartition des Volumes d'Actions",
                            width=400,  # Largeur réduite
                            height=200  # Hauteur réduite
                        )

                        st.altair_chart(circle_chart_volume, use_container_width=True)


                    st.divider()

                elif selected_tab == 'Predictions':
                    st.subheader("Stock Price Forecast")
                    st.divider()
                    
                   # Forecasting prices using ARIMA model
                    df_historical['Date'] = pd.to_datetime(df_historical['Date'])
                    df_historical.set_index('Date', inplace=True)

                    model = ARIMA(df_historical['Close'], order=(1, 1, 1))
                    model_fit = model.fit()
                    forecast = model_fit.forecast(steps=3)

                    forecast_dates = pd.date_range(start=pd.to_datetime('now'), periods=3)
                    predicted_prices = forecast.values

                    # Render predicted prices in cards
                    cols = st.columns(3)  # Create three columns for the cards
                    for i, price in enumerate(predicted_prices):
                        with cols[i]:  # Use the current column for each price
                            ui.card(
                                title=f"Price for {forecast_dates[i].date()}",
                                content=f"{price:.2f}",  # Format the price to two decimal places
                                description="Forecasted price based on historical data",
                                key=f"forecast_{i+1}"
                            ).render()

                    # Forecast Line Chart
                    forecast_df = pd.DataFrame({'Date': forecast_dates, 'Predicted Close Price': predicted_prices})
                    combined_df = pd.concat([df_historical[['Close']], forecast_df.set_index('Date')])
                    st.line_chart(combined_df)
                    
                elif selected_tab == 'Chatbot':
                    st.title("🤖 Trade Analyst Agent")
                    chatbot_page()
        else:
            st.error("Company not found in the JSON file.")
