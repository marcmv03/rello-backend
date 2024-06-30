# board/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404, JsonResponse
from .models import Board
from .board_serializer import BoardSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class BoardListCreateView(APIView):
    """
    View to list all boards and create a new board.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self,request, format=None):
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        profile  = request.user 
        board_data = request.data
        #add  profile to data
        board_data['profile'] = profile.id
        serializer = BoardSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        board = serializer.create(request.data)
        board.save()
        serializer = BoardSerializer(board)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BoardDetailView(APIView):
    """
    View to retrieve, update, or delete a board instance.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise Http404

    def get(self, pk):
        board = self.get_object(pk)
        serializer = BoardSerializer(board)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        board = self.get_object(pk)
        user = request.user
        if board.profile != user:
            return Response({"error": "You are not authorized to update this board"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = BoardSerializer(board, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        board = serializer.update(board, request.data)
        board.save()
        serializer = BoardSerializer(board)
    
    def delete(self,request,pk):
        try:
            board = self.get_object(pk)
            board.delete()
            id = board.id
            user = request.user
            if board.profile != user:
                return Response({"error": "You are not authorized to delete this board"}, status=status.HTTP_401_UNAUTHORIZED)
            return JsonResponse({"id": id })
        except Board.DoesNotExist:
            raise Http404

