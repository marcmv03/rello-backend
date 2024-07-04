from django.db import models
from board.models import Board

# Create your models here.
class List(models.Model):
    name = models.CharField(max_length=100,null=False ,blank=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE,null=False)
    position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name