
from board.models import Board
from .models import List
from rest_framework import serializers
class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id','name','board']
    def create(self, validated_data):
        name = validated_data['name']
        board_id  = validated_data['board']
        board = Board.objects.get(id = board_id)
        position = board.num_lists+1 
        list = List.objects.create(name=name,board = board,position= position) 
        return list 
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        return instance.save()
