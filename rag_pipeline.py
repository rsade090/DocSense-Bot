import os
from dotenv import load_dotenv
import openai
from search_engine import SearchEngine


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class RAGPipeline:
    def __init__(self):
        
        self.search_engine = SearchEngine()

    def retrieve_relevant_text(self, query, search_type):
        
        if search_type == "Keyword":
            return self.search_engine.search_keyword(query)
        else:  # Semantic Search
            return self.search_engine.search_semantic(query)

    def generate_answer_openai(self, query, context, chat_history):
       #Stream an answer from OpenAI GPT-4o using chat history for better context.
        if not OPENAI_API_KEY:
            raise ValueError("Missing OpenAI API Key. Set it in the .env file.")

        client = openai.OpenAI(api_key=OPENAI_API_KEY)  

        
        messages = [{"role": "system", "content": "You are an AI assistant with access to the text extracted from the user's uploaded PDF(s) and HTML webpages.\
            You can reference that text to answer questions. If asked whether you have access to the PDF, URL or HTML websites, you do have its contents (extracted text) provided in your context,\
                but you do not have direct file-system access to read or write files.. please be polite and helpful. you have to provide the answer organizely and output \
                    in the markdown when necessary so that make it easier for user to get the response."}]

                        
                
        for user_query, ai_response in chat_history:
            messages.append({"role": "user", "content": user_query})
            messages.append({"role": "assistant", "content": ai_response})
        
        
        messages.append({"role": "user", "content": f"Context: {context}\n\nPrevious Questions: {', '.join([q for q, _ in chat_history])}\n\nCurrent Question: {query}\n\nAnswer:"})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            stream=True  # Enable streaming
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


    def generate_answer(self, query, search_type, chat_history):
        #Retrieve relevant text and stream an answer 
        relevant_texts = self.retrieve_relevant_text(query, search_type)
        
        if not relevant_texts or not isinstance(relevant_texts, list):
            relevant_texts = ["No relevant context found."]

        context = " ".join(relevant_texts)[:3000]  # Truncate context to avoid token limits

        
        return self.generate_answer_openai(query, context, chat_history)
      

