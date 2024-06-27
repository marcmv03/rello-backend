from django.urls import path
from .views import ProfileCreateView,ProfileView

urlpatterns = [
    path('profiles', ProfileCreateView.as_view(), name='profiles_list'),
    path('profiles/<int:id>', ProfileView.as_view(), name='profile_detail'),
]