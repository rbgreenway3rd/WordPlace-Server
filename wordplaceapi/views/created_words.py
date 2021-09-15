"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.contrib.auth.models import User  # pylint:disable=imported-auth-user
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from wordplaceapi.models import CreatedWords  # pylint:disable=imported-auth-user


class CreatedWordsSerializer(serializers.ModelSerializer):
    """JSON serializer for user-created words"""
    class Meta:
        model = CreatedWords
        url = serializers.HyperlinkedIdentityField(
            view_name='user', lookup_field='id')
        fields = ('id', 'user', 'word', 'pronunciation',
                  'definition', 'partOfSpeech', 'example')
        # depth = 1


class CreatedWordsView(ViewSet):
    """Request handlers for CreatedWords in the WordPlace Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    """WordPlace: user-created words"""

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

    def create(self, request):
        """
        @api {POST} /createdwords POST new user-created word
        @apiName CreatedWord
        """

        new_created_word = CreatedWords()
        new_created_word.user = User.objects.get(
            id=request.auth.user.id)
        new_created_word.word = request.data["word"]
        new_created_word.pronunciation = request.data["pronunciation"]
        new_created_word.definition = request.data["definition"]
        new_created_word.partOfSpeech = request.data["partOfSpeech"]
        new_created_word.example = request.data["example"]

        new_created_word.save()

        serializer = CreatedWordsSerializer(
            new_created_word, context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        @api {PUT} /createdwords/:id PUT changes the created_word
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        created_word = CreatedWords.objects.get(pk=pk)
        created_word.user = User.objects.get(
            id=request.auth.user.id)
        created_word.word = request.data["word"]
        created_word.pronunciation = request.data["pronunciation"]
        created_word.definition = request.data["definition"]
        created_word.partOfSpeech = request.data["partOfSpeech"]
        created_word.example = request.data["example"]

        created_word.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single created_word

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            created_word = CreatedWords.objects.get(pk=pk)
            created_word.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except CreatedWords.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
