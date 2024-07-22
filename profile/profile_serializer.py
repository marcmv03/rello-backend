# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'username','password','email','first_name','last_name', 'bio']
#create profile.If the user already exits throw exception
    def create(self, validated_data) :
        email  = validated_data.get('email')
        if Profile.objects.filter(email=email).exists():
            raise serializers.ValidationError('Profile already exists')
        password = validated_data.get('password')
         #pop password to data
        validated_data.pop('password')
        result =  Profile.objects.create(**validated_data)
        User.set_password(self=result,raw_password= password)
        result.save()
        return result
#update profile
    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance
        