from .models import List
from rest_framework import serializers
class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = '__all__'
    #function to get all id's of the lists that belongs to a board
    def get_list_ids(self, instance):
        return instance.lists.values_list('id', flat=True)
    def create(self, validated_data):
        return List.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        return instance
