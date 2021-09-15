"""View module for handling requests about user-favorited words"""
from django.http import HttpResponseServerError
from django.contrib.auth.models import User  # pylint:disable=imported-auth-user
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from wordplaceapi.models import FavoritedWords  # pylint:disable=imported-auth-user


class FavoritedWordsSerializer(serializers.ModelSerializer):
    """JSON serializer for user-favorited words"""
    class Meta:
        model = FavoritedWords
        url = serializers.HyperlinkedIdentityField(
            view_name='user', lookup_field='id')
        fields = ('id', 'uuid', 'user', 'word',
                  'definition', 'partOfSpeech', 'link')
        # depth = 1


class FavoritedWordsView(ViewSet):
    """Request handlers for FavoritedWords in the WordPlace Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    """WordPlace: user-favorited words"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single FavoritedWord (favorited_word)

        Returns:
            Response -- JSON serialized FavoritedWord (favorited_word)
        """
        try:
            favorited_word = FavoritedWords.objects.get(pk=pk)
            serializer = FavoritedWordsSerializer(
                favorited_word, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all favorited_words

        Returns:
            Response -- JSON serialized list of favorited_words
        """
        favorited_words = FavoritedWords.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = FavoritedWordsSerializer(
            favorited_words, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """
        @api {POST} /favoritedwords POST new user-favorited word
        @apiName FavoritedWord
        """

        new_favorited_word = FavoritedWords()
        new_favorited_word.uuid = request.data["uuid"]
        new_favorited_word.user = User.objects.get(
            id=request.auth.user.id)
        new_favorited_word.word = request.data["word"]
        new_favorited_word.definition = request.data["definition"]
        new_favorited_word.partOfSpeech = request.data["partOfSpeech"]
        new_favorited_word.link = request.data["link"]

        new_favorited_word.save()

        serializer = FavoritedWordsSerializer(
            new_favorited_word, context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        @api {PUT} /favoritedwords/:id PUT changes the favorited_word
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        favorited_word = FavoritedWords.objects.get(pk=pk)
        favorited_word.uuid = request.data["uuid"]
        favorited_word.user = User.objects.get(
            id=request.auth.user.id)
        favorited_word.word = request.data["word"]
        favorited_word.definition = request.data["definition"]
        favorited_word.partOfSpeech = request.data["partOfSpeech"]
        favorited_word.link = request.data["link"]

        favorited_word.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single favorited_word

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            favorited_word = FavoritedWords.objects.get(pk=pk)
            favorited_word.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except FavoritedWords.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
