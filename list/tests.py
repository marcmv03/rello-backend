from django.test import TestCase
from django.contrib.auth.models import User
from profile.models import Profile  # Adjust this import based on your app structure
from board.models import Board
from list.models import List
from list.list_serializer import ListSerializer

class ListPositionUpdateTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # Create a test profile associated with the test user
        self.profile = Profile.objects.create(user=self.user, other_profile_fields='values')  # Adjust field names and values as necessary
        
        # Create a test board associated with the test profile
        self.board = Board.objects.create(name='Test Board', description='A board for testing', profile=self.profile)  # Adjust the 'profile' field as necessary
        
        # Create five lists associated with the test board, with positions 0 through 4
        self.lists = [List.objects.create(name=f'Test List {i}', board=self.board, position=i) for i in range(5)]

    def test_update_position_greater(self):
        list_to_update = self.lists[0]
        new_position = 3
        ListSerializer.update_positions(list_to_update, new_position)
        self.assertEqual(List.objects.get(id=list_to_update.id).position, new_position)
        # Additional assertions to check if other lists' positions have been adjusted correctly

    def test_update_position_lesser(self):
        list_to_update = self.lists[4]
        new_position = 1
        ListSerializer.update_positions(list_to_update, new_position)
        self.assertEqual(List.objects.get(id=list_to_update.id).position, new_position)
        # Additional assertions to check if other lists' positions have been adjusted correctly

    def test_update_position_out_of_range(self):
        list_to_update = self.lists[2]
        new_position = -1
        with self.assertRaises(ValueError):
            ListSerializer.update_positions(list_to_update, new_position)

    def test_update_position_unchanged(self):
        list_to_update = self.lists[2]
        new_position = 2
        ListSerializer.update_positions(list_to_update, new_position)
        self.assertEqual(List.objects.get(id=list_to_update.id).position, new_position)
        # Additional assertions to ensure no other lists' positions have changed