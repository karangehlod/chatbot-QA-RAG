# documents/services/langchain_service.py
import openai
from django.conf import settings
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import PostgreSQL
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
import logging

logger = logging.getLogger(__name__)

# Set OpenAI API key and endpoint (for Azure OpenAI, configure similarly)
openai.api_key = settings.AZURE_OPENAI_API_KEY
openai.api_base = settings.AZURE_OPENAI_ENDPOINT
MODEL_NAME = "text-embedding-ada-002"

class LangChainService:
    """
    Service class for generating embeddings and performing query-based retrieval.
    """

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.AZURE_OPENAI_API_KEY,
            openai_api_base=settings.AZURE_OPENAI_ENDPOINT,
            model_name=MODEL_NAME
        )

    def generate_embeddings(self, text_chunks):
        """
        Generate embeddings for the text chunks.
        """
        try:
            embeddings = self.embeddings.embed_documents(text_chunks)
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    def query_documents(self, query, vector_store):
        """
        Perform query-based retrieval from the vector store.
        """
        try:
            # Retrieve the most relevant chunks based on the query
            retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
            retrieval_chain = ConversationalRetrievalChain.from_llm(
                llm=openai.Completion.create(model=MODEL_NAME, prompt=query),
                retriever=retriever
            )
            response = retrieval_chain.run(input=query)
            return response
        except Exception as e:
            logger.error(f"Error querying documents: {str(e)}")
            raise