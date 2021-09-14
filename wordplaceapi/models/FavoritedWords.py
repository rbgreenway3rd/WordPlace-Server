from django.db import models
from django.contrib.auth.models import User  # pylint:disable=imported-auth-user


class FavoritedWords(models.Model):
    # uuid = models.UUIDField(
    #     primary_key=False,
    #     editable=False,
    #     Null=False,
    # )
    uuid = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # foreign key
    word = models.CharField(max_length=30)
    definition = models.CharField(max_length=200)
    partOfSpeech = models.CharField(max_length=20)
    link = models.CharField(max_length=200)
