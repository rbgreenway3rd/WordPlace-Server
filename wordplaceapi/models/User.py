from django.db import models
from django.contrib.auth.models import User  # pylint:disable=imported-auth-user


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
