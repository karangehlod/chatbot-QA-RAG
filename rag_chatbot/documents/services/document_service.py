# documents/services/document_service.py
import os
from PyPDF2 import PdfReader
from django.conf import settings
import logging

from documents.models import DocumentEmbeddings

logger = logging.getLogger(__name__)

class DocumentService:
    """
    Service class to handle document upload and processing.
    """

    def validate_file_type(self, file):
        """
        Validates if the uploaded file is a PDF.
        """
        if not (file.name.endswith('.pdf') or file.name.endswith('.txt')):
            raise ValueError("Only PDF files are allowed.")

    def save_uploaded_file(self, file):
        """
        Save the uploaded file to the server.
        """
        try:
            upload_dir = os.path.join(settings.BASE_DIR, 'uploaded_files')
            os.makedirs(upload_dir, exist_ok=True)  # Ensure the directory exists
            file_path = os.path.join(upload_dir, file.name)
            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            return file_path
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise e

    def extract_text_from_pdf(self, file_path):
        """
        Extract text from a PDF file.
        """
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise e

    def chunk_text(self, text, chunk_size=1000):
        """
        Break the text into smaller chunks to fit token limits.
        """
        chunks = []
        text_length = len(text)
        for i in range(0, text_length, chunk_size):
            chunks.append(text[i:i+chunk_size])
        return chunks
    
    def store_embeddings_in_db(self, chunks, embeddings):
        """
        Store the embeddings in the database.
        """
        for chunk, embedding in zip(chunks, embeddings):
            # Assuming you have a model named DocumentEmbedding
            DocumentEmbeddings.objects.create(
                text=chunk,
                embedding=embedding
            )
    
    def chunk_text_for_token_limit(self, text, token_limit=512):
            """
            Chunk the text to handle token limits.
            """
            # This is a simple example. You might need to adjust the logic based on your tokenization requirements.
            words = text.split()
            chunks = []
            current_chunk = []
    
            for word in words:
                if len(current_chunk) + len(word) + 1 > token_limit:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = [word]
                else:
                    current_chunk.append(word)
    
            if current_chunk:
                chunks.append(' '.join(current_chunk))
    
            return chunks