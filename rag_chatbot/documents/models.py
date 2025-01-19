# documents/models.py
from django.db import models

class Document(models.Model):
    text = models.TextField()
    embedding = models.JSONField()  # Store the embedding (can also be VECTOR if pgvector)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.id} uploaded at {self.uploaded_at}"