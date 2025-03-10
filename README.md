# DocSense bot

##  Overview

DocSense Bot is a Streamlit-based web application that leverages **Retrieval Augmented Generation (RAG)**, integrating semantic and keyword-based search for efficient information retrieval. It utilizes **Whoosh** for keyword-based search and **ChromaDB** for vector-based semantic search, combined with **OpenAI's GPT-4o** for generative response generation. The system processes **PDF and HTML webpages**, enabling users to extract meaningful insights through real-time queries.

### Key Components
- **Whoosh**: Optimized for high-speed, full-text keyword search.
- **ChromaDB**: Handles dense vector-based semantic search.
- **LangChain**: Manages document processing and query transformation.
- **Streamlit**: Provides an interactive, minimal-latency user interface.

##  Features

- **Hybrid Search Mechanism**: Supports both **keyword-based** (lexical) and **semantic** (vectorized) search.
- **Adaptive Chunking & Indexing**: Implements dynamic document segmentation for optimized retrieval.
- **Streaming Response Generation**: Real-time AI-powered answer streaming via GPT-4o.
- **Scalable Architecture**: Efficient document processing with parallel indexing.
- **File Ingestion Support**: Accepts **PDF and HTML webpages** for analysis.

##  Installation
Install dependencies, set up API keys, and run the project:

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_openai_api_key
streamlit run app.py
```

## Usage Guide

1️⃣ **Upload a document (PDF/HTML) or provide a URL.**  
2️⃣ **Select search mode:**  **Keyword-based Search** (Exact term matching)  and  **Semantic Search** (Contextual understanding)  
3️⃣ **Query the document in natural language.**  
4️⃣ **Receive AI-generated answers in real time.**  



