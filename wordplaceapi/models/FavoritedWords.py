from django.db import models
from .User import User


class FavoritedWords(models.Model):
    uuid = models.UUIDField(
        primary_key=False,
        editable=False,
        Null=False,
    )
    userId = models.OneToOneField(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=30)
    definition = models.CharField(max_length=50)
    partOfSpeech = models.CharField(max_length=20)
    link = models.CharField(max_length=200)
