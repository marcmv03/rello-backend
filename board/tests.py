from profile.models import Profile
from django.test import TestCase
#write a test to try board serializer.Create  and instance of a board and then,create two lists,associate with them and try that the serializer
#return the board with the lists
from board.models import Board
from list.models import List
from board.board_serializer import BoardSerializer

# Create your tests heree.
class BoardModelTestCase(TestCase):
    def setUp(self):
        self.board_name = "Test Board"
        self.board_description = "A board for testing"
        self.profile = Profile.objects.create(username="testuser", password="testpassword")
        self.board = Board.objects.create(name=self.board_name, description=self.board_description,profile = self.profile)
        #save board and list
        self.list = List.objects.create(name="Test List", board=self.board, position=1)
    #try to serialize a board with a list
    def test_serializer_can_create_a_board(self):
        serializer = BoardSerializer(self.board)
        self.assertEqual(serializer.data["name"], self.board_name)
        self.assertEqual(serializer.data["description"], self.board_description)
        self.assertEqual(serializer.data["profile"], self.profile.id)
        list_ids = serializer.data["list_ids"]
        print(list_ids)
        self.assertEqual(self.list.id, list_ids[0])
    #test board serializer with null values
    def test_serializer_with_null_values(self) :
        serializer = BoardSerializer(data={"name": None, "description": None})
        self.assertFalse(serializer.is_valid())