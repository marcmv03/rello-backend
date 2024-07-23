from django.test import TestCase
from django.contrib.auth.models import User
from profile.models import Profile  # Adjust this import based on your app structure
from board.models import Board
from list.models import List
from list.list_serializer import ListSerializer

class ListPositionUpdateTestCase(TestCase):
    def setUp(self):
        # Create a test user
        
        # Create a test profile associated with the test user
        self.profile = Profile.objects.create(username = "Test-user",first_name ="test",last_name = "test",email="test@example.com",bio="test-bio")  # Adjust field names and values as necessary
        
        # Create a test board associated with the test profile
        self.board = Board.objects.create(name='Test Board', description='A board for testing', profile=self.profile)  # Adjust the 'profile' field as necessary
        
        # Create five lists associated with the test board, with positions 0 through 4
        self.lists = [List.objects.create(name=f'Test List {i}', board=self.board, position=i) for i in range(5)]
        self.board.num_lists = 5
        self.board.save()

    def test_update_position_greater(self):
        list_to_update = self.lists[0]
        new_position = 3
        ListSerializer.update_positions(list_to_update, new_position)
        self.assertEqual(List.objects.get(id=list_to_update.id).position, new_position)
        for l in self.lists:
            #check that lists with positions between the old and new positions have been adjusted
            if l.position > list_to_update.position and l.position <= new_position:
                self.assertEqual(List.objects.get(id=l.id).position, l.position - 1)
        # Additional assertions to check if other lists' positions have been adjusted correctly
            self.lists = List.objects.filter(board=self.board).order_by('position')

    def test_update_position_lesser(self):
        list_to_update = self.lists[4]
        new_position = 1
        ListSerializer.update_positions(list_to_update, new_position)
        self.assertEqual(List.objects.get(id=list_to_update.id).position, new_position)
        # Additional assertions to check if other lists' positions have been adjusted correctly
        #same as the last case but adjusting to this case
        for l in self.lists:
            if l.position < list_to_update.position and l.position >= new_position:
                self.assertEqual(List.objects.get(id=l.id).position, l.position + 1)
        self.lists = List.objects.filter(board=self.board).order_by('position')

    def test_update_position_out_of_range(self):
        list_to_update = self.lists[2]
        new_position = -1
        with self.assertRaises(ValueError):
            ListSerializer.update_positions(list_to_update, new_position)

    def test_update_position_unchanged(self):
        list_to_update = self.lists[2]
        new_position = 2
        ListSerializer.update_positions(list= list_to_update, new_position=new_position)
        self.assertEqual(List.objects.get(id=list_to_update.id).position, new_position)
        # Additional assertions to ensure no other lists' positions have changed
        self.lists = List.objects.filter(board=self.board).order_by('position')
        for i, l in enumerate(self.lists):
            self.assertEqual(l.position, i)