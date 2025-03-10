import streamlit as st
from document_loader import DocumentLoader
from search_engine import SearchEngine
from rag_pipeline import RAGPipeline
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
import os
import shutil
import chromadb
import requests


def clean_html(raw_text):
    """Remove unwanted HTML tags from text."""
    soup = BeautifulSoup(raw_text, "html.parser")
    return soup.get_text()


search_engine = SearchEngine()
rag_pipeline = RAGPipeline()


st.markdown(
    """
    <style>
        /* Modern Dark Mode Styling */
        .stApp {
            background-color: #10141A;
            color: #E0E0E0;
        }
        .sidebar .sidebar-content {
            background-color: #1A1F29;
            padding: 15px;
            border-radius: 10px;
        }
        /* Customizing Text Input */
        .stTextInput>div>div>input {
            background-color: #1F2733;
            color: white;
            border-radius: 8px;
            border: 1px solid #1e3a5f;
            padding: 10px;
        }
        /* Custom Buttons */
        .stButton>button {
            background-color: #1e3a5f;  /* Navy Blue */
            color: white;
            border-radius: 10px;
            padding: 10px 15px;
            border: none;
            font-weight: bold;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #142a4f;  /* Darker Navy Blue on Hover */
        }
        /* Custom Radio Buttons */
        div[data-testid="stRadio"] label {
            color: #E0E0E0;
        }
        /* Headers */
        h1, h2, h3, h4 {
            color: #1e3a5f;
        }
        /* Customizing Markdown */
        .stMarkdown {
            color: #E0E0E0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)



st.markdown(
    """
    <style>
    /* Override the default sidebar width */
    [data-testid="stSidebar"] {
        min-width: 220px !important;
        max-width: 220px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* Approach A: For older Streamlit versions */
    .main .block-container {
        padding-top: 1rem !important;
    }

    /* Approach B: A more recent Streamlit class name */
    .css-1cpxqw2 {
        padding-top: 1rem !important;
    }

    /* Approach C: Another class name seen in newer versions */
    .css-18e3th9 {
        padding-top: 1rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Welcome to Content Navigator!")

# Initialize chat history 
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []  
if "selected_question" not in st.session_state:
    st.session_state["selected_question"] = None  

st.sidebar.header("Setting")
input_type = st.sidebar.radio("Input Type", ["PDF", "Link"], key="input_type")

if "previous_input_type" not in st.session_state:
    st.session_state["previous_input_type"] = input_type

if input_type != st.session_state["previous_input_type"]:
    st.session_state["chat_history"] = []
    st.session_state["selected_question"] = None
    st.session_state["previous_input_type"] = input_type
    st.rerun()


if input_type == 'Link':
    
    input_data = st.text_input(f"Enter the URL")


    if input_data.strip():

        try:
            if "last_uploaded_file" not in st.session_state or st.session_state["last_uploaded_file"] != input_data:


                if os.path.exists("index"):
                    shutil.rmtree("index")
                st.session_state["chat_history"] = []
                st.session_state["selected_question"] = None 
                st.session_state["last_uploaded_file"] = input_data  
                st.rerun() 
                        
            loader = WebBaseLoader(input_data)
            documents = loader.load()
            loader = DocumentLoader(documents)
            extracted_text = loader.extract_text()
            search_engine.add_document_to_keyword_index(extracted_text)
            search_engine.add_document_to_semantic_index(extracted_text)

        except requests.exceptions.MissingSchema:
            st.error("Please enter a valid URL (e.g., include https://).")

elif input_type == 'PDF':
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf", "html", "htm"], key="file_upload")
        
    if uploaded_file is not None:
        if "last_uploaded_file" not in st.session_state or st.session_state["last_uploaded_file"] != uploaded_file.name:
           
            if os.path.exists("index"):
                shutil.rmtree("index")
      
            st.session_state["chat_history"] = [] 
            st.session_state["selected_question"] = None 
            st.session_state["last_uploaded_file"] = uploaded_file.name
            st.rerun()

            search_engine.init_keyword_search()
            search_engine.init_semantic_search()

        loader = DocumentLoader(uploaded_file)
        extracted_text = loader.extract_text()

        search_engine.add_document_to_keyword_index(extracted_text)
        search_engine.add_document_to_semantic_index(extracted_text)



search_type = st.sidebar.radio("Search Type", ["Semantic","Keyword"], key="search_type")

chat_container = st.container()
with chat_container:
    for i, (question, answer) in enumerate(st.session_state["chat_history"]):

        st.markdown(f"""
        <div style="
            display: inline-block;
            background-color: #1e3a5f;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            color: white;
            max-width: 70%;
            word-wrap: break-word;
        ">
            {question}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="text-align: left; background-color: #2a2d35; padding: 10px; border-radius: 10px; margin: 5px 80px 5px 40px; color: white;">
                <b></b> {answer}
        """, unsafe_allow_html=True)


unique_key = f"search_input_{len(st.session_state['chat_history'])}"
search_query = st.text_input("Type your query and press Enter...", key=unique_key)

if search_query:
    if search_type == "Keyword":
        response_stream = search_engine.search_keyword(search_query)
    else:
        response_stream = rag_pipeline.generate_answer(search_query, search_type, st.session_state["chat_history"])

    st.session_state["chat_history"].append((search_query, ""))
    response_index = len(st.session_state["chat_history"]) - 1  

    response_placeholder = st.empty()
    streamed_response = ""

    for chunk in response_stream:

        streamed_response += chunk
        response_placeholder.markdown(streamed_response, unsafe_allow_html=True)

    st.session_state["chat_history"][response_index] = (search_query, streamed_response)
    st.rerun()
