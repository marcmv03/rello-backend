from django.shortcuts import render

# Create your views here.
# board/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from models import Profile

from profilePage.serializers import ProfileSerializer, UserSerializer
class ProfileView(APIView) :
      permission_classes = [IsAuthenticated]
      authentication_classes = [JWTAuthentication]
      def get(self,request,id, format=None):
            profile = Profile.objects.get(id=id)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        
        #update a profile,the only fileds to update can be username,first_name,last_name and bio.Use the serializers
      def put(self,request,id,format=None):
           #update profile
              user = User.objects.get(id=id)
              user_serializer = UserSerializer(user,data=request.data)
              if user_serializer.is_valid():
                    user_serializer.save()
                    profile = Profile.objects.get(user=user)
                    profile_serializer = ProfileSerializer(profile,data=request.data)
                    if profile_serializer.is_valid():
                        profile_serializer.update(profile,request.data)
                        return Response(profile_serializer.data)
              
class ProfileCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self,request,format=None):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            profile_serializer = ProfileSerializer(data=request.data)
            if profile_serializer.is_valid():
                profile_serializer.save(user=user)
                return Response(profile_serializer.data)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
                

            

   
