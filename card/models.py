from django.db import models

# Create your models here.
class Card(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    board_id = models.BigIntegerField()
    list_id = models.BigIntegerField()
    position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
