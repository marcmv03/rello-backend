#import user model from django
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Profile(User):
    """
    Model for user profile.
    """
    bio = models.TextField(blank=True)
