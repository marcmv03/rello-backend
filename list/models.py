from django.db import models
from board.models import Board

# Create your models here.
class List(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE,null=True)
    position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name