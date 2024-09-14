from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    message = models.TextField(max_length=200)
    author = models.TextField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
