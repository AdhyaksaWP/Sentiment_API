from rest_framework import serializers

class SentimentSerializer(serializers.Serializer):
    message = serializers.CharField()
