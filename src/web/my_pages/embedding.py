import streamlit as st
import requests
import os
import sys
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import ArxivLoader

st.title('Embedding')

OLLAMA_SERVER = os.getenv("OLLAMA_SERVER", "http://localhost:11434")

arxiv_id = st.text_input("Arxiv paper ID")
if st.button("Load"):
    arxiv_docs = ArxivLoader(query=arxiv_id).load()
    st.json(arxiv_docs[0].metadata)
    st.session_state["arxiv_docs"] = arxiv_docs
    arxiv_docs_full_text = arxiv_docs[0].page_content
    st.session_state["arxiv_docs_full_text"] = arxiv_docs_full_text

if "arxiv_docs" in st.session_state:
    if "openai_api_key" not in st.session_state:
        st.warning("Please enter your OpenAI API key.")
    if "Embedding_model" not in st.session_state:
        st.warning("Please select a Embedding model.")

    if st.button("Create Graph RAG's Embedding"):

        with st.status("Running the Graph RAG's Indexer..."):
            
            st.write("Getting OpenAI API key...")
            openai_api_key = st.session_state["openai_api_key"]

            st.write("Creating file for Graph RAG's indexer...")
            os.mkdir("tmp")
            os.mkdir("tmp/input")

            with open("tmp/input/input.txt", "w") as f:
                f.write(arxiv_docs_full_text)

            st.write("Initializing Graph RAG's indexer...")
            os.system(f"python3 -m graphrag.index --init --root ./tmp")
            os.system(f"rm -rf tmp/.env")

            with open("tmp/.env", "w") as f:
                f.write(f"GRAPHRAG_API_KEY={openai_api_key}")

            st.write("Running the Graph RAG's Indexing pipeline...")
            result = os.system(f"python3 -m graphrag.index --root ./tmp")

            if result != 0:
                st.error("Graph RAG's Indexer has failed.")
            else:
                st.success("Graph RAG's Indexer has finished running.")

    if st.button("Create OLLAMA's Embedding"):

        with st.status("Running the OLLAMA's Indexer..."):

            st.write("Getting Embedding model...")
            embedding_model = st.session_state["Embedding_model"]

            st.write("Getting Arxiv Full Text...")
            arxiv_docs_full_text = st.session_state["arxiv_docs_full_text"]

            st.write("Creating Ollama embeddings...")
            embeddings = OllamaEmbeddings(model=embedding_model,base_url=OLLAMA_SERVER)
            
            st.write("Embedding the Arxiv Full Text...")
            vector_store = FAISS.from_texts(embeddings, arxiv_docs_full_text)

            st.write("Storing the embeddings...")
            directorys = os.listdir()
            if "ollama_tmp" not in directorys:
                os.mkdir("ollama_tmp")
            vector_store.save_local("embeddings/" + arxiv_id)

if 'tmp' in os.listdir() and st.button("Delete tmp folder"):
    os.system("rm -rf tmp")
    st.success("tmp folder has been deleted.")