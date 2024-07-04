# board/serializers.py
from rest_framework import serializers

from list.models import List
from .models import Board
class BoardSerializer(serializers.ModelSerializer):
    list_ids = serializers.SerializerMethodField("find_list_ids")
    def find_list_ids(self,instance):
        #get all the lists that belongs to a board
        lists = List.objects.filter(board=instance)
        lists_ids = []
        for list in lists:
            lists_ids.append(list.id)
        return lists_ids

    class Meta:
        model = Board
        fields = ['id', 'name', 'description','list_ids','profile']
    def update(self, instance, validated_data):
        return Board.objects.update(instance, validated_data)
    def create(self, validated_data):
        board = Board.objects.create(**validated_data)
        return board   
