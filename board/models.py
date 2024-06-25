from django.db import models
#user from django
from profilePage.models import Profile

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    profile  = models.ForeignKey(Profile, on_delete=models.CASCADE)
