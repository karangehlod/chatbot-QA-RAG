# documents/tasks.py
from celery import shared_task
from .services.document_service import DocumentService
from .services.langchain_service import LangChainService
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def process_document_task(self, file_path):
    """
    Task to process a document asynchronously: extract text, chunk it, generate embeddings.
    """
    try:
        document_service = DocumentService()
        langchain_service = LangChainService()

        # Extract text from PDF
        text = document_service.extract_text_from_pdf(file_path)

        # Chunk text to handle token limits
        chunks = document_service.chunk_text_for_token_limit(text)

        # Generate embeddings
        embeddings = langchain_service.generate_embeddings(chunks)

        # Store the embeddings in the database
        document_service.store_embeddings_in_db(chunks, embeddings)

        logger.info(f"Document {file_path} processed successfully.")
        return True
    except Exception as e:
        logger.error(f"Error processing document {file_path}: {str(e)}")
        raise