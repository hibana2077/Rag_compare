import streamlit as st

st.title('Settings')

OPENAI_API_KEY = st.text_input("OpenAI API Key", type="password")

if st.button("Save"):
    st.session_state["openai_api_key"] = OPENAI_API_KEY
    st.success("API Key saved.")

CHAT_MODEL = st.selectbox("Chat Model", ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo","gpt-4o","gpt-3.5-turbo-16k"], index=0)

if st.button("Save"):
    st.session_state["chat_model"] = CHAT_MODEL
    st.success("Chat Model saved.")