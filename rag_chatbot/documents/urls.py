# documents/urls.py
from django.urls import path
from .views import DocumentUploadView, QueryView

urlpatterns = [
    path('upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('query/', QueryView.as_view(), name='query'),  # Add query endpoint
]