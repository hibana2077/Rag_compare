import streamlit as st
import requests
import os
import sys
import pandas as pd
import tiktoken
import subprocess

st.title('Chat')

if "graphrag_chat_messages" not in st.session_state:
    st.session_state["graphrag_chat_messages"] = []

if "ollama_chat_messages" not in st.session_state:
    st.session_state["ollama_chat_messages"] = []

def graphrag_chat(prompt: str, mode: str = "global") -> str:
    
    command_global_template = f'python3 -m graphrag.query --root ./tmp --method global "{prompt}"' if mode == "global" else f'python3 -m graphrag.query --root ./tmp --method local "{prompt}"'
    process = subprocess.Popen(command_global_template, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    response = stdout.decode("utf-8")
    if mode == "global":
        response = response.split("SUCCESS: Global Search Response:")[-1]
    else:
        response = response.split("SUCCESS: Local Search Response:")[-1]
    
    return response

OLLAMA_SERVER = os.getenv("OLLAMA_SERVER", "http://localhost:11434")

graphrag_tab, normalrag_tab = st.tabs(["GraphRAG", "NormalRAG"])

with graphrag_tab:
    if "tmp" not in os.listdir():
        st.warning("Please run the GraphRAG's Embedding first.")
    else:
        for message in st.session_state["graphrag_chat_messages"]:
            with st.chat_message(message['role']):
                st.markdown(message['content'])

        mode = st.radio("Mode", ["global", "local"])
        
        prompt = st.chat_input("Please enter your question:")

        if prompt:
            st.session_state.graphrag_chat_messages.append({"role": "user", "content": prompt})

            with st.status("Running the GraphRAG's Chat..."):
                response = graphrag_chat(prompt, mode)

            st.session_state.graphrag_chat_messages.append({"role": "assistant", "content": response})

        for message in st.session_state["graphrag_chat_messages"]:
            with st.chat_message(message['role']):
                st.markdown(message['content'])

with normalrag_tab:
    if "ollama_tmp" not in os.listdir():
        st.warning("Please run the OLLAMA's Embedding first.")
    else:
        st.warning("NormalRAG is not implemented yet.")