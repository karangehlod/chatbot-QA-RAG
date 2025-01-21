from .services.document_service import DocumentService
from .services.langchain_service import LangChainService
import logging

logger = logging.getLogger(__name__)


def process_document_task(file_path):
    """
    Task to process a document asynchronously: extract text, chunk it, generate embeddings.
    """
    try:
        document_service = DocumentService()
        langchain_service = LangChainService()

        # check file is pdf or text file
        if file_path.endswith('.pdf'):
            text = document_service.extract_text_from_pdf(file_path)
        elif file_path.endswith('.txt'):
            with open(file_path, 'r') as f:
                text = f.read()
        else:
            raise ValueError("Only PDF and text files are allowed.")
        

        # Chunk text to handle token limits
        chunks = document_service.chunk_text_for_token_limit(text)

        # Generate embeddings
        embeddings = langchain_service.generate_embeddings(chunks)

        # Store embeddings in the database
        document_service.store_embeddings_in_db(chunks, embeddings)

    except Exception as e:
        logger.error(f"Error processing document: {e}")
        raise e