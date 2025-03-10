import os
import time
import whoosh.index as index
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser
import chromadb
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
import re
import streamlit as st  
from langchain.text_splitter import CharacterTextSplitter
from whoosh import highlight






load_dotenv()

INDEX_DIR = "index"

class SearchEngine:
    def __init__(self):
        
        self.init_keyword_search()
        self.init_semantic_search()

    def init_keyword_search(self):
        #Set up Whoosh keyword search index
        schema = Schema(content=TEXT(stored=True)) 

        if not os.path.exists(INDEX_DIR):
            os.mkdir(INDEX_DIR)

        if not index.exists_in(INDEX_DIR):
            index.create_in(INDEX_DIR, schema)

        try:
            self.whoosh_index = index.open_dir(INDEX_DIR)
        except index.LockError:
            print(" Whoosh index is locked. Removing lock file and retrying")
            self._remove_lock_file()
            self.whoosh_index = index.open_dir(INDEX_DIR)

    def _remove_lock_file(self):
        
        lock_file = os.path.join(INDEX_DIR, "_LOCK")
        if os.path.exists(lock_file):
            os.remove(lock_file)
            print("Lock file removed.")

    def add_document_to_keyword_index(self, text):
        
        # chunk_size = 300  # Adjust chunk size (characters)
        # text_chunks = [text[i:i+chunk_size].strip() + " " for i in range(0, len(text), chunk_size)]
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        text_chunks = splitter.split_text(text)

        max_retries = 3
        for attempt in range(max_retries):
            try:
                writer = self.whoosh_index.writer()
                for chunk in text_chunks:
                    writer.add_document(content=chunk)
                writer.commit()
                return
            except index.LockError:
                print(f" Whoosh index is locked (attempt {attempt+1}/{max_retries}). Retrying in 1s...")
                self._remove_lock_file()
                time.sleep(1)
        raise RuntimeError("Failed to acquire Whoosh lock after multiple attempts.")

    def search_keyword(self, query):

        with self.whoosh_index.searcher() as searcher:
            query_parser = QueryParser("content", self.whoosh_index.schema)
            parsed_query = query_parser.parse(query)
            results = searcher.search(parsed_query, limit=10)

            if not results:
                return [f'No exact match found for "{query}".']

            
            frag = highlight.ContextFragmenter(surround=60, maxchars=500)
            frag.maxfrags = None  # Allow multiple fragments if the chunk has multiple matches
            results.fragmenter = frag

            all_matched_sentences = []

            for r in results:
                snippet = r.highlights("content")
                if not snippet.strip():
                    snippet = r["content"]

                sentences = re.split(r'(?<=[.!?])\s+', snippet.strip())

                for s in sentences:
                    if query.lower() in s.lower():
                        all_matched_sentences.append(s.strip())

            seen = set()
            unique_matched_sentences = []
            for s in all_matched_sentences:
                if s not in seen:
                    seen.add(s)
                    unique_matched_sentences.append(s)

            count = len(unique_matched_sentences)

            if count == 0:
                
                return [f'No exact match found for "{query}".']

            
            list_items = "".join(f"<li>{sentence}</li>" for sentence in unique_matched_sentences)
            final_html = f"""
    <p>The word "<strong>{query}</strong>" is found <strong>{count}</strong> times in the uploaded file.</p>
    <ol>
        {list_items}
    </ol>
    """
            return [final_html]

    def init_semantic_search(self):
    
        self.embedding_model = OpenAIEmbeddings()
        self.chroma_client = chromadb.Client()
        self.vectorstore = Chroma(
            client=self.chroma_client,
            collection_name="documents",
            embedding_function=self.embedding_model
        )

    def add_document_to_semantic_index(self, text):
        
        self.vectorstore.add_texts([text])

    def search_semantic(self, query):
        
        results = self.vectorstore.similarity_search(query, k=5)
        return [r.page_content for r in results]
