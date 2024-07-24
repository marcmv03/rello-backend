from django.shortcuts import render

# Create your views here.
from profile.models import Profile
from list.models import List
from .models import Card
from .card_serializer import CardSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse

class CardCreateView(APIView):
    """
    View to list all cards for a list and create a new card.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, list_id, format=None):
        try:
            list_instance = List.objects.get(id=list_id)
            cards = Card.objects.filter(list_id=list_instance.id).order_by('position')
            serializer = CardSerializer(cards, many=True)
            return Response(serializer.data)
        except List.DoesNotExist:
            return Response({"error": "List not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, list_id, format=None):
        try:
            profile = Profile.objects.get(id=request.user.id)
            list_instance = List.objects.get(id=list_id)
            board = list_instance.board
            if board.profile != profile:
                return Response({"error": "You are not authorized to add a card to this list"}, status=status.HTTP_401_UNAUTHORIZED)
            card_data = dict(request.data)
            card_data['list_id'] = list_instance.id
            serializer = CardSerializer(data=card_data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            card_instance = serializer.create(card_data)
            return Response({"id": card_instance.id}, status=status.HTTP_201_CREATED)
        except List.DoesNotExist:
            return Response({"error": "List not found"}, status=status.HTTP_404_NOT_FOUND)

class CardDetailView(APIView):
    """
    View to retrieve, update, or delete a card instance.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Card.objects.get(pk=pk)
        except Card.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        try:
            card = Card.objects.get(id=id)
            serializer = CardSerializer(card)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Card.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, format=None):
        try:
            card_instance = self.get_object(id)
            user = request.user
            profile = Profile.objects.get(id=user.id)
            list_instance = card_instance.list_id
            board = list_instance.board
            card_data = dict(request.data)
            card_data['list_id'] = list_instance.id
            if board.profile != profile:
                return Response({"error": "You are not authorized to update this card"}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = CardSerializer(card_instance, data=card_data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.update(instance=card_instance, validated_data=card_data)
            return Response(serializer.data)
        except Card.DoesNotExist:
            return Response({"error": "Card not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid position"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        try:
            card_instance = self.get_object(id)
            user = request.user
            profile = Profile.objects.get(id=user.id)
            list_instance = card_instance.list_id
            board = list_instance.board
            if board.profile != profile:
                return Response({"error": "You are not authorized to delete this card"}, status=status.HTTP_401_UNAUTHORIZED)
            position = card_instance.position
            card_instance.delete()
            cards_list = Card.objects.filter(list_id=list_instance, position__gt=position)
            for card in cards_list:
                card.position = card.position - 1
                card.save()
            return JsonResponse({"id": id})
        except Card.DoesNotExist:
            return Response({"error": "Card not found"}, status=status.HTTP_404_NOT_FOUND)
