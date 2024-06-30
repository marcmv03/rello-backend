# Description: This file contains the URL patterns for the board app.
from django.urls import path
from  board.views import BoardListCreateView, BoardDetailView


urlpatterns = [
    path('boards/', BoardListCreateView.as_view(), name='board-list-create'),
    path('boards/<int:pk>', BoardDetailView.as_view(), name='board-detail')
]