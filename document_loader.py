
from bs4 import BeautifulSoup
from PIL import Image
import io
import pdfplumber
from langchain.text_splitter import CharacterTextSplitter
import pdfplumber
import re


class DocumentLoader:
    def __init__(self, uploaded_file):
        self.uploaded_file = uploaded_file
        
        if hasattr(uploaded_file, "name"):
            self.file_type = uploaded_file.name.split(".")[-1].lower()
        else:
            self.file_type = "link"


    def extract_text(self):
        
        if self.file_type == "pdf":
            return self.extract_text_from_pdf()
        elif self.file_type == "link":
            return self.extrac_text_from_link()
        elif self.file_type in ["html", "htm"]:
            return self.extract_text_from_html()
        else:
            raise ValueError("Unsupported file format. Only PDF and HTML are allowed.")


    def clean_text(self,text):

        text = BeautifulSoup(text, "html.parser").get_text()  # Remove any HTML tags
        text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
        return text

    def extract_text_from_pdf(self):
        
        text = []

        with pdfplumber.open(self.uploaded_file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text(layout=True, x_tolerance=2.0, y_tolerance=2.0)
                if extracted:
                    cleaned_text = self.clean_text(extracted)  # Clean text
                    text.append(cleaned_text)
                else:
                    text.append("No text found")

        return "\n\n".join(text).strip()





    def extrac_text_from_link(self):
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        texts = text_splitter.split_documents(self.uploaded_file)
        texts = [str(doc.page_content) for doc in texts]
        return  " ".join(texts)
    
    def extract_text_from_html(self):
        
        content = self.uploaded_file.read().decode("utf-8")
        soup = BeautifulSoup(content, "html.parser")
        text = soup.get_text(separator="\n")
        return text.strip()
