import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

st.set_page_config(page_title="Raiyan AI Chatbot", page_icon="🤖")

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("API Key missing! Please set GOOGLE_API_KEY in your .env file.")
    st.stop()

if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=api_key)

st.title("🤖 Raiyan AI Chatbot")

if "chat_session" not in st.session_state:
    st.session_state.chat_session = st.session_state.client.chats.create(model="gemini-3.6-flash")
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message here..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = st.session_state.chat_session.send_message(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
            
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        if "503" in str(e) or "UNAVAILABLE" in str(e):
            st.warning("Google's servers are temporarily busy right now. Please wait a moment and try sending your message again.")
        else:
            st.error(f"Error communicating with Gemini: {e}")
