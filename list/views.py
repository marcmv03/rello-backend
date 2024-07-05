# list/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404, JsonResponse

from profilePage.models import Profile
from .models import List, Board
from .list_serializer import ListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class ListCreateView(APIView):
    """
    View to list all lists for a board and create a new list.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, board_id, format=None):
        try:
            board = Board.objects.get(id=board_id)
            lists = List.objects.filter(board=board)
            serializer = ListSerializer(lists, many=True)
            return Response(serializer.data)
        except Board.DoesNotExist:
            return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, board_id, format=None):
        try:
            print(board_id)
            profile = Profile.objects.get(id = request.user.id )
            board = Board.objects.get(id=board_id)
            if board.profile != profile:
                return Response({"error": "You are not authorized to add a list to this board"}, status=status.HTTP_401_UNAUTHORIZED)
            list_data = dict(request.data)
            list_data['board'] = board.id
            print(list_data)
            serializer = ListSerializer(data=list_data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            list_instance = serializer.create(list_data)
            board.num_lists = board.num_lists +1 
            board.save() 
            return Response({"id": list_instance.id}, status=status.HTTP_201_CREATED)
        except Board.DoesNotExist:
            return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

class ListDetailView(APIView):
    """
    View to retrieve, update, or delete a list instance.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return List.objects.get(pk=pk)
        except List.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        try:
            board = Board.objects.get(id=id)
            lists = List.objects.filter(board=board)
            serializer = ListSerializer(lists, many=True)
            return Response(serializer.data)
        except Board.DoesNotExist:
            return Response({"error": "Board not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, format=None):
        try:
            list_instance = self.get_object(id)
            user = request.user
            board = list_instance.board
            if board.profile != user:
                return Response({"error": "You are not authorized to update this list"}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = ListSerializer(list_instance, data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            list_instance = serializer.save()
            return Response(serializer.data)
        except List.DoesNotExist:
            return Response({"error": "List not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id, format=None):
        try:
            list_instance = self.get_object(id)
            user = request.user
            profile = Profile.obje
            board = list_instance.board
            if board.profile != user:
                return Response({"error": "You are not authorized to delete this list"}, status=status.HTTP_401_UNAUTHORIZED)
            list_instance.delete()
            board.num_lists = board.num_lists -1 
            return JsonResponse({"id": id})
        except List.DoesNotExist:
            return Response({"error": "List not found"}, status=status.HTTP_404_NOT_FOUND)
