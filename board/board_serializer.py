# board/serializers.py
from rest_framework import serializers
from .models import Board
class BoardSerializer(serializers.ModelSerializer):
    list_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='lists')
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'list_ids']
    def update(self, instance, validated_data):
        return Board.objects.update(instance, validated_data)
    def create(self, validated_data):
        return Board.objects.create(**validated_data)  
