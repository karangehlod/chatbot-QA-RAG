# Generated by Django 5.1.5 on 2025-01-19 17:46

import pgvector.django.vector
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('embedding', pgvector.django.vector.VectorField(dimensions=1536)),
            ],
        ),
    ]
