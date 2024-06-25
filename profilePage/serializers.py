# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
#create user
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
#update user,only username,first name and last name
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio']
#create profile.If the user already exits throw exception
    def create(self, validated_data):
        user = validated_data.get('user')
        if Profile.objects.filter(user=user).exists():
            raise serializers.ValidationError('Profile already exists')
        return Profile.objects.create(**validated_data)
#update profile
    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance
        