from rest_framework import serializers
from .models import Card
from rello.utils import update_positions

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

    def create(self, validated_data):
        card =  Card.objects.create(**validated_data)
        card.position = card.list.num_cards +1 

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        new_position = validated_data.get('position', instance.position)
        update_positions(instance, new_position, 'list')
        instance.save()
        return instance