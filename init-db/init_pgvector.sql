CREATE EXTENSION IF NOT EXISTS vector;

-------------------
CREATE TABLE document_documents (
    id SERIAL PRIMARY KEY,
    text TEXT,
    embedding VECTOR(1536),  -- Assuming you are using the pgvector extension for vector fields
    metadata TEXT
);
-----------------
CREATE INDEX document_documents_embedding_idx ON document_documents USING ivfflat(embedding);