
from board.models import Board
from .models import List
from rest_framework import serializers
class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = '__all__'
    position = serializers.IntegerField(required = False) 
    def update_positions(instance,new_position):
        if new_position != None:
            if new_position < 0 or  new_position >= instance.board.num_lists:
                raise ValueError()
            original_position = instance.position 
            if new_position > original_position :
                lists_to_shift_down = List.objects.filter(board = list.board,position__lte = new_position)
                for lists in lists_to_shift_down:
                    list.position = list.position -1 
                    list.save()
            elif new_position < original_position:
                lists_to_shift_up = List.objects.filter(board=list.board,position__gte = new_position)
                for lists in lists_to_shift_up :
                    list.position = list.position +1 
                    list.save() 
                instance.position = new_position 
    
    def create(self, validated_data):
        name = validated_data['name']
        board_id  = validated_data['board']
        board = Board.objects.get(id = board_id)
        position = board.num_lists+1 
        list = List.objects.create(name=name,board = board,position= position) 
        return list 
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        new_position = validated_data['position']
        self.update_position(new_position= new_position,instance = instance)
        return instance.save()
