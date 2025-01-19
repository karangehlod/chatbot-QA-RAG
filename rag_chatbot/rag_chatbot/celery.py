# rag_chatbot/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rag_chatbot.settings')

app = Celery('rag_chatbot')

# Configure Celery using the settings in the Django project
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks in all registered Django app configs
app.autodiscover_tasks()