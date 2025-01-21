from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
import openai
from django.conf import settings
from pgvector.sqlalchemy import Vector
from sqlalchemy import create_engine, Column, Integer, String, JSON, Table, MetaData
from sqlalchemy.orm import sessionmaker
import logging
from asgiref.sync import async_to_sync

from documents.models import DocumentEmbeddings


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
        self.embeddings = AzureOpenAIEmbeddings(
            openai_api_version=settings.AZURE_OPENAI_EMBEDDING_VERSION,
            openai_api_type='azure',
            api_key=settings.AZURE_OPENAI_EMBEDDING_API_KEY,
            azure_endpoint=settings.AZURE_OPENAI_EMBEDDING_ENDPOINT,
            azure_deployment=settings.AZURE_OPENAI_EMBEDDING_MODEL
        )

        self.llm = AzureChatOpenAI(
            openai_api_type='azure',
            azure_deployment=settings.AZURE_OPENAI_GPT_MODEL,
            api_key=settings.AZURE_OPENAI_API_KEY,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_version=settings.AZURE_OPENAI_GPT_VERSION,
            temperature=0.7,
            max_tokens=100
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
    
    def llm_interaction(self, query, response):
        """
        Generate response from the language model.
        """
        try:
            # Construct context
            context = " ".join(response)
            
            # Generate response with Azure OpenAI
            llm = AzureChatOpenAI(
                openai_api_type='azure',
                azure_deployment=settings.AZURE_OPENAI_GPT_MODEL,
                api_key=settings.AZURE_OPENAI_API_KEY,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                api_version=settings.AZURE_OPENAI_GPT_VERSION,
                temperature=0.7,
                max_tokens=4096
            )
            
            # Construct prompt with context
            messages = [
                {"role": "system", "content": """You are a helpful assistant that answers questions based on provided context. Follow these Instructions:
                1. Provide answer based only on context and relevent fetched data.
                2. Do not provide any information that is not present in the context.
                3. Provide response proper after removing uncessary characters and keep information in paragraph of 50 words only.
                4. For any query which don't have answer or confused, provide 'No answer found' response."""},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
            ]
            
            response = llm.invoke(messages)
            return response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
    def generate_embeddings_query(self, query):
        """
        Generate embeddings for the query .
        """
        try:
            embeddings = self.embeddings.embed_query(query)
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise

    def query_documents(self, query, session, document_embeddings):
        """
        Query documents based on the query embedding.
        """
        try:
            # Generate embedding for the query
            query_embedding = self.generate_embeddings_query(query)

            query_embedding = [float(x) for x in query_embedding]

            # Retrieve the most relevant chunks based on the query embedding
            results = DocumentEmbeddings.objects.raw(
                'SELECT * FROM document_embeddings ORDER BY embedding <-> CAST(%s AS vector) LIMIT 3',
                [query_embedding]
            )

            response = [result.text for result in results]
            return response
        except Exception as e:
            logger.error(f"Error querying documents: {str(e)}")
            raise

    def get_vector_store(self):
        """
        Returns a PostgreSQL vector store initialized with embeddings.
        """
        # Make sure to configure your Postgres connection URL
        postgres_url = f"postgresql://{settings.DATABASES['default']['USER']}:" \
                       f"{settings.DATABASES['default']['PASSWORD']}@" \
                       f"{settings.DATABASES['default']['HOST']}:" \
                       f"{settings.DATABASES['default']['PORT']}/{settings.DATABASES['default']['NAME']}"
        
        # Initialize SQLAlchemy engine and session
        engine = create_engine(postgres_url)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Define the table structure
        metadata = MetaData()
        document_embeddings = Table(
            'documents_embedding', metadata,
            Column('id', Integer, primary_key=True),
            Column('text', String),
            Column('embedding', Vector(1536))
        )

        # Create the table if it doesn't exist
        metadata.create_all(engine)

        return session, document_embeddings