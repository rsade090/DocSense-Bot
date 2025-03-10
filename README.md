# Content-Navigator

# 📚 Retrieval Augmented Generation (RAG) Application

## 🚀 Overview

This project is an advanced **Retrieval Augmented Generation (RAG) system** that integrates **semantic and keyword-based search** for efficient information retrieval. It leverages **Whoosh** for keyword-based search and **ChromaDB** for vector-based semantic search, combined with **OpenAI's GPT-4o** for generative response generation. The system processes **PDF and HTML documents**, enabling users to extract meaningful insights through real-time queries.

### Key Components
- **Whoosh**: Optimized for high-speed, full-text keyword search.
- **ChromaDB**: Handles dense vector-based semantic search.
- **LangChain**: Manages document processing and query transformation.
- **Streamlit**: Provides an interactive, minimal-latency user interface.

## 🛠 Features

- **Hybrid Search Mechanism**: Supports both **keyword-based** (lexical) and **semantic** (vectorized) search.
- **Adaptive Chunking & Indexing**: Implements dynamic document segmentation for optimized retrieval.
- **Streaming Response Generation**: Real-time AI-powered answer streaming via GPT-4o.
- **Scalable Architecture**: Efficient document processing with parallel indexing.
- **File Ingestion Support**: Accepts **PDF and HTML webpages** for analysis.

## 🔧 Installation
Install dependencies, set up API keys, and run the project:
```bash
pip install -r requirements.txt
env
OPENAI_API_KEY=your_openai_api_key
streamlit run app.py
```
Configure OpenAI API key in a **.env** file:
```env
OPENAI_API_KEY=your_openai_api_key

```

### 3️⃣ Run the Application
```bash
streamlit run app.py
```
Access the interface at `http://localhost:8501`.

## 📝 Usage Guide

1️⃣ **Upload a document (PDF/HTML) or provide a URL.**
2️⃣ **Select search mode:**
   - **Keyword-based Search** (Exact term matching)
   - **Semantic Search** (Contextual understanding)
3️⃣ **Query the document in natural language.**
4️⃣ **Receive AI-generated answers in real time.**

## ⚡ Performance Enhancements

- **Optimized Query Pipeline**: Reduces latency through batch embeddings.
- **Efficient Index Management**: Minimizes disk I/O overhead.
- **Real-time Adaptive Response Streaming**: Uses incremental token generation.
- **Token Usage Optimization**: Restricts context window to essential document segments.




