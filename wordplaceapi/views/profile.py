"""View module for handling requests about user Profiles"""
from wordplaceapi.views import created_words
from wordplaceapi.models.CreatedWords import CreatedWords
from wordplaceapi.models.Profile import Profile
from django.http import HttpResponseServerError
from django.contrib.auth.models import User  # pylint:disable=imported-auth-user
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from wordplaceapi.models import Profile  # pylint:disable=imported-auth-user


class ProfileView(ViewSet):
    """Request handlers for user profile info in the WordPlace Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):

        try:

            current_user = User.objects.get(user=request.auth.user)
            # created_words = CreatedWords.objects.all()
            # current_user.created_words = CreatedWords.objects.filter(user=created_words.user)
            current_user.created_words = CreatedWords.objects.filter(
                user=current_user)

            serializer = ProfileSerializer(
                current_user, many=False, context={'request': request})

            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customer profile

    Arguments:
        serializers
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        depth = 1


class CreatedWordsSerializer(serializers.ModelSerializer):
    """JSON serializer for user-created words"""
    class Meta:
        model = CreatedWords
        url = serializers.HyperlinkedIdentityField(
            view_name='user', lookup_field='id')
        fields = ('id', 'user', 'word', 'pronunciation',
                  'definition', 'partOfSpeech', 'example')
        depth = 1


class ProfileSerializer(serializers.ModelSerializer):
    """JSON serializer for customer profile

    Arguments:
        serializers
    """
    user = UserSerializer(many=False)
    created_words = CreatedWordsSerializer(many=True)

    class Meta:
        model = Profile
        fields = ('user', 'created_words')
        depth = 1
