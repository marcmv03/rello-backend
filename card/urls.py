from django.urls import path
from .views import CardCreateView,CardDetailView



urlpatterns = [
   path('lists/<int:id>/cards/', CardCreateView.as_view(), name='card-list'),
   path('cards/<int:id>/', CardDetailView.as_view(), name='card-detail'),

]