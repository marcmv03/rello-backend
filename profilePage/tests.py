from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

class ProfileModelTest(TestCase):
    def setUp(self):
        # Create a user instance for testing
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, bio='This is a test bio.')

    def test_profile_creation(self):
        # Test that the profile instance has been created
        self.assertTrue(isinstance(self.profile, Profile))

    def test_profile_bio(self):
        # Test setting and getting the bio field
        self.assertEqual(self.profile.bio, 'This is a test bio.')
        # Update the bio
        self.profile.bio = 'Updated bio.'
        self.profile.save()
        # Fetch the updated profile and test the updated bio
        updated_profile = Profile.objects.get(id=self.profile.id)
        self.assertEqual(updated_profile.bio, 'Updated bio.')

