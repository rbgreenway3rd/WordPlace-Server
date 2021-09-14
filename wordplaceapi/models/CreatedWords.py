from django.db import models
from django.contrib.auth.models import User  # pylint:disable=imported-auth-user


class CreatedWords(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=30)
    pronunciation = models.CharField(max_length=40)
    definition = models.CharField(max_length=200)
    partOfSpeech = models.CharField(max_length=20)
    example = models.CharField(max_length=100)
