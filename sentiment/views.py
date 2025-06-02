from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SentimentSerializer
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Initialize stopword remover
factory = StopWordRemoverFactory()
stopword_remover = factory.create_stop_word_remover()

# Load IndoBERTweet Sentiment Model
MODEL_NAME = "./sentiment_project/model"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Sentiment labels
id2label = {
    0: "Positive",
    1: "Neutral",
    2: "Negative"
}

class SentimentAnalysisView(APIView):
    def post(self, request):
        serializer = SentimentSerializer(data=request.data)
        if serializer.is_valid():
            original_text = serializer.validated_data['message']

            # Remove stopwords
            clean_text = stopword_remover.remove(original_text)

            # Tokenize input
            inputs = tokenizer(clean_text, return_tensors="pt", truncation=True)

            # Predict
            with torch.no_grad():
                logits = model(**inputs).logits
                prediction = torch.argmax(logits, dim=-1).item()

            sentiment = id2label[prediction]

            return Response({
                'original_text': original_text,
                'clean_text': clean_text,
                'sentiment': sentiment
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
