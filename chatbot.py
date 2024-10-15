import os
import streamlit as st
import pandas as pd
import google.generativeai as genai

# Directly assign the API key
API_KEY = "AIzaSyAKy5IlwYtvV1xgzApDPXsi9W-C2oPoq_o"

def get_chatbot_response(user_question: str) -> str:
    genai.configure(api_key=API_KEY)

    # Load both datasets
    historical_df = pd.read_csv("Data/historical_data.csv")
    news_df = pd.read_csv("Data/Processed_Company_News.csv")

    # Prepare the context for the prompt
    detailed_prompt = (
        "Hello! I am a chatbot specializing in stock market insights and company news. "
        "I can answer financial questions, give advice, and provide recommendations based on the data you provide. "
        "Feel free to ask any questions regarding the stock market, and I'll do my best to assist you!\n\n"
        f"{user_question}\n"
    )

    # Call the Gemini model for a response
    response = genai.generate_text(
        prompt=detailed_prompt,
        model='gemini-pro',  # Make sure this is the correct model name
        temperature=0.3,
        max_output_tokens=150  # Adjust if necessary
    )

    return response.text.strip()

def chatbot_page():
    st.write("## Chatbot")
    st.caption("🚀 A Streamlit chatbot powered by Google Gemini with expertise in stock market analysis")

    if API_KEY:
        st.write("You can now use the chatbot.")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_prompt = st.chat_input("Ask An Expert...")

        if user_prompt:
            st.chat_message("user").markdown(user_prompt)
            st.session_state.chat_history.append({"role": "user", "content": user_prompt})

            response = get_chatbot_response(user_prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

            with st.chat_message("assistant"):
                st.markdown(response)
    else:
        st.write("**API key not found.**")

# Run the chatbot page
if __name__ == "__main__":
    chatbot_page()
