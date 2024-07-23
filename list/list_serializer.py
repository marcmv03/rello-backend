
from board.models import Board
from .models import List
from rest_framework import serializers
class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = '__all__'
    position = serializers.IntegerField(required = False) 
    def  update_positions(self,list,new_position):
        if new_position != None:
            if new_position < 0 or  new_position >= list.board.num_lists:
                raise ValueError()
            original_position = list.position 
            if new_position > original_position :
                lists_to_shift_down = List.objects.filter(board = list.board,
                                                         position__gt = original_position,position__lte = new_position)
                for l in lists_to_shift_down:
                    l.position = l.position -1 
                    l.save()
            elif new_position < original_position:
                lists_to_shift_up = List.objects.filter(board=list.board,position__gte = new_position,position__lt = original_position)
                for l in lists_to_shift_up :
                    l.position = l.position +1 
                    l.save() 
            list.position = new_position 
            list.save()
    
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
            self.update_positions(instance,position)
        instance.name = validated_data.get('name', instance.name)
        return instance.save()
