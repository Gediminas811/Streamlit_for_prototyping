# To run a code : streamlit run streamlit-genai.py

import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables

token = os.getenv("SECRET_GEMINI")  # Replace with your actual token
endpoint = "https://models.github.ai/inference"
model = "gemini-2.5-flash"

# initialize the Google GenAI client
client = genai.Client(api_key=token)

st.title("Echo Bot")

if "messages" not in st.session_state:
    st.session_state.messages = [
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("What is up?")
# React to user input
if prompt:
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    prompt_text = "You are a helpful assistant.\n" + "\n".join([m["content"] for m in st.session_state.messages])
    # call to Google GenAI API
    # Note: The Google GenAI client is initialized with the API key. 
    response = client.models.generate_content(
        model=model,
        contents=[prompt_text]
    )

    response_text = response.text
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response_text)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})