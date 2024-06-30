from .models import List
from rest_framework import serializers
class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = '__all__'
    def create(self, validated_data):
        return List.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        return instance
