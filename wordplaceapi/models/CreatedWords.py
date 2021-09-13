from django.db import models
from .User import User


class CreatedWords(models.Model):
    userId = models.OneToOneField(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=30)
    pronunciation = models.CharField(max_length=40)
    definition = models.CharField(max_length=50)
    partOfSpeech = models.CharField(max_length=20)
    example = models.CharField(max_length=100)
