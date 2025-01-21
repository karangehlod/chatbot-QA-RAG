from django.conf import settings
from django.core.cache import cache
from langchain_openai import AzureChatOpenAI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .services.document_service import DocumentService
from .services.langchain_service import LangChainService
import logging
from .tasks import process_document_task

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

            # Process the document asynchronously
            process_document_task(file_path)

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
            # Create the LangChain service and query the documents
            langchain_service = LangChainService()

            # Initialize the vector store and retrieve documents
            session, document_embeddings = langchain_service.get_vector_store()

            # Query documents and retrieve response
            responsedb = langchain_service.query_documents(query, session, document_embeddings)

            # Generate response based on context
            response = langchain_service.llm_interaction(query, responsedb)
            
            return JsonResponse({
                "response": response.content,
                "context_used": bool(response)
            })


        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)