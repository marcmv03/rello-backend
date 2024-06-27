# Description: This file contains the test cases for the Profile model and ProfileSerializer.
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .models import Profile
from .serializers import ProfileSerializer

class ProfileSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'bio': 'This is a test bio.',
            'password': 'testpassword123'
        }

    def test_create_profile(self):
        serializer = ProfileSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        profile = serializer.create(serializer.validated_data)
        self.assertEqual(profile.username, self.user_data['username'])
        self.assertEqual(profile.email, self.user_data['email'])
        self.assertEqual(profile.first_name, self.user_data['first_name'])
        self.assertEqual(profile.last_name, self.user_data['last_name'])
        self.assertEqual(profile.bio, self.user_data['bio'])

    def test_update_profile(self):
        profile = Profile.objects.create_user(**self.user_data)
        update_data = {
            'username': 'extinguisheduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'bio': 'This is an updated bio.',
            'email':'extinguisheduser@example.com',
            'password': 'testPassword123'        }
        serializer = ProfileSerializer(data=update_data)
        self.assertTrue(serializer.is_valid())
        profile = serializer.update(profile, update_data)
        self.assertEqual(profile.first_name, update_data['first_name'])
        self.assertEqual(profile.last_name, update_data['last_name'])
        self.assertEqual(profile.bio, update_data['bio'])

    def test_create_invalid_profile(self):
        invalid_data = self.user_data.copy()
        invalid_data['email'] = 'invalidemail'
        serializer = ProfileSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

