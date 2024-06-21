from django.db import models
#user from django
from django.contrib.auth.models import User

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)
