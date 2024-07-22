from django.urls import path
from list.views import ListCreateView,ListDetailView
urlpatterns = [
    path('boards/<int:board_id>/lists', ListCreateView.as_view(), name='list'),
    path('lists/<int:id>/', ListDetailView.as_view(), name='list_detail'),
    #path('list/<int:id>/change/', views.list_change, name='list_change'),
] 