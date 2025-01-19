# documents/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .services.document_service import DocumentService
from .services.langchain_service import LangChainService
from .models import Document
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class DocumentUploadView(APIView):
    """
    Handle document uploads and processing.
    """

    def post(self, request):
        uploaded_file = request.FILES.get('file', None)

        if not uploaded_file:
            return JsonResponse({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Validate and save the uploaded file
            document_service = DocumentService()
            document_service.validate_file_type(uploaded_file)
            file_path = document_service.save_uploaded_file(uploaded_file)

            # Extract text and chunk it
            extracted_text = document_service.extract_text_from_pdf(file_path)
            chunks = document_service.chunk_text(extracted_text)

            # Generate embeddings for the text chunks
            langchain_service = LangChainService()
            embeddings = langchain_service.generate_embeddings(chunks)

            # Store the document and its embeddings in the database
            for i, chunk in enumerate(chunks):
                Document.objects.create(text=chunk, embedding=embeddings[i])

            return JsonResponse({"message": "File uploaded and processing started."}, status=status.HTTP_202_ACCEPTED)
        
        except Exception as e:
            logger.error(f"Error uploading document: {str(e)}")
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class QueryView(APIView):
    """
    Handle user queries by embedding the query and retrieving relevant document chunks.
    """

    def post(self, request):
        query = request.data.get('query', None)

        if not query:
            return JsonResponse({"error": "No query provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the response for the query is cached
            cached_response = cache.get(query)
            if cached_response:
                return JsonResponse({"response": cached_response}, status=status.HTTP_200_OK)

            # Create the LangChain service and query the documents
            langchain_service = LangChainService()

            # Fetch all documents from the database
            vector_store = PostgreSQL.from_documents(Document.objects.all(), langchain_service.embeddings)

            # Query documents and retrieve response
            response = langchain_service.query_documents(query, vector_store)

            # Cache the result to avoid recomputation
            cache.set(query, response, timeout=3600)  # Cache for 1 hour

            return JsonResponse({"response": response}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)