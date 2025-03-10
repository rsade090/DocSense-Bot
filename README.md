# Content-Navigator

# 📚 Retrieval Augmented Generation (RAG) Application

## 🚀 Overview

This project is a **Retrieval Augmented Generation (RAG) system** designed to process and extract insights from uploaded documents using **semantic and keyword-based search**. It leverages **OpenAI's GPT-4o** for response generation and supports **document ingestion from PDFs and HTML web pages**.

The application is built with:

- **Whoosh** for keyword-based search
- **ChromaDB** for semantic retrieval
- **LangChain** for document processing
- **Streamlit** for an intuitive web-based interface

## 🛠 Features

- 🔍 **Dual Search Mode**: Supports both **keyword-based** and **semantic** search.
- 📝 **Document Upload & Indexing**: Allows users to upload **PDFs and HTML webpages**.
- 🌐 **Streaming Output**: Real-time response streaming for a seamless user experience.
- ⚡ **Optimized Performance**: Efficient indexing and retrieval mechanisms.

## 📎 Project Structure

```
├── app.py               # Streamlit-based frontend for user interaction
├── search_engine.py     # Implements keyword (Whoosh) and semantic (ChromaDB) search
├── rag_pipeline.py      # RAG pipeline integrating retrieval and response generation
├── document_loader.py   # Handles text extraction from PDFs and HTML
├── .env                 # Stores API keys (not included for security reasons)
```

## 🏠 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/rag-application.git
cd rag-application
```

### 2️⃣ Set Up Environment

Ensure **Python 3.8+** is installed. Install dependencies:

```bash
pip install -r requirements.txt
```

Create a **.env** file for OpenAI API:

```env
OPENAI_API_KEY=your_openai_api_key
```

### 3️⃣ Run the Application

```bash
streamlit run app.py
```

Access the web interface at `http://localhost:8501`.

## 📝 Usage

1️⃣ **Upload a PDF or enter a website URL**\
2️⃣ **Select search type** (Keyword or Semantic)\
3️⃣ **Ask questions** based on the document\
4️⃣ **Get real-time AI-generated answers**

## 🏆 Enhancements & Optimizations

- ✅ **Chunked Document Processing** for better retrieval efficiency
- ✅ **Real-time Streaming Responses** using GPT-4o
- ✅ **Search Performance Enhancements** (indexing optimizations)

## 📌 Future Improvements

- 🔄 Support for additional file formats (e.g., Word, Markdown)
- 🎯 Fine-tuning retrieval quality using hybrid search techniques
- 🏃️ Caching for improved performance

## 🐜 License

MIT License © 2025

---

🌟 **Built by [Your Name]** – Passionate about AI & NLP!

