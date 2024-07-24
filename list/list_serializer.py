
from board.models import Board
from .models import List
from rest_framework import serializers
from rello.utils import update_positions
class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = '__all__'
    name = serializers.CharField(max_length=100) 
    position = serializers.IntegerField(required=False) 
    def create(self, validated_data):
        name = validated_data['name']
        board_id  = validated_data['board']
        board = Board.objects.get(id = board_id)
        position = board.num_lists+1 
        list = List.objects.create(name=name,board = board,position= position) 
        return list 
    def update(self, instance, validated_data):
        name = validated_data['name']
        position = validated_data['position']
        if name != None:
            instance.name = name
        if position != None:
            update_positions(instance,position,'board')
        instance.name = validated_data.get('name', instance.name)
        return instance.save()
