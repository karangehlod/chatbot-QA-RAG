from rest_framework import serializers

class DocumentSerializer(serializers.Serializer):
    document = serializers.FileField()

class QuerySerializer(serializers.Serializer):
    query = serializers.CharField()