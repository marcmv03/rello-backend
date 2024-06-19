from django.test import TestCase
#write a test to try board serializer.Create  and instance of a board and then,create two lists,associate with them and try that the serializer
#return the board with the lists
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from board.models import Board
from list.models import List
from board.board_serializer import BoardSerializer

# Create your tests here.
class BoardModelTestCase(TestCase):
    def setUp(self):
        self.board_name = "Test Board"
        self.board_description = "A board for testing"
        self.board = Board.objects.create(name=self.board_name, description=self.board_description)
        #save board and list
        self.list = List(name="Test List", board=self.board, position=1)
    #try to serialize a board with a list
    def test_serializer_can_create_a_board(self):
        serializer = BoardSerializer(self.board)
        self.assertEqual(serializer.data["name"], self.board_name)
        self.assertEqual(serializer.data["description"], self.board_description)
        self.assertEqual(serializer.data["lists"][0], self.list.id)
    #test get all boards
    def test_api_can_get_all_boards(self):
        client = APIClient()
        response = client.get(reverse("board-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    #test get a specific board
    def test_api_can_get_a_board(self):
        self.list.save() 
        client = APIClient()
        response = client.get(reverse("board-detail", kwargs={"pk": self.board.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

