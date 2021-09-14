"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from wordplaceapi.models import CreatedWords


class CreatedWordsSerializer(serializers.ModelSerializer):
    """JSON serializer for user-created words"""
    class Meta:
        model = CreatedWords
        fields = ('id', 'user', 'word', 'pronunciation',
                  'definition', 'partOfSpeech', 'example')


class CreatedWordsView(ViewSet):
    """WordPlace user-created words"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single CreatedWord (created_word)

        Returns:
            Response -- JSON serialized CreatedWord (created_word)
        """
        try:
            created_word = CreatedWords.objects.get(pk=pk)
            serializer = CreatedWordsSerializer(
                created_word, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all created_words

        Returns:
            Response -- JSON serialized list of created_words
        """
        created_words = CreatedWords.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = CreatedWordsSerializer(
            created_words, many=True, context={'request': request})
        return Response(serializer.data)
