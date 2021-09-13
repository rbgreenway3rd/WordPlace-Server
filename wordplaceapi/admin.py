from django.contrib import admin
from .models import FavoritedWords
from .models import CreatedWords

# Register your models here.

admin.site.register(FavoritedWords)
admin.site.register(CreatedWords)
