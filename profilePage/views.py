from django.shortcuts import render

# Create your views here.
# board/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Profile

from profilePage.serializers import ProfileSerializer
class ProfileView(APIView) :
      permission_classes = [IsAuthenticated]
      authentication_classes = [JWTAuthentication]
      def get(self,request,id, format=None):
        try:
            profile = Profile.objects.get(id=id)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        #update a profile,the only fileds to update can be username,first_name,last_name and bio.Use the serializers
      def put(self,request,id,format=None):
           #update profile
            profile = Profile.objects.get(id = id )
            profile_serializer = ProfileSerializer(profile,data=request.data)
            if profile_serializer.is_valid():
                profile_serializer.update(profile,request.data)
                return Response(profile_serializer.data)
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
              
class ProfileCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self,request,format=None):
            profile_serializer = ProfileSerializer(data=request.data)
            if profile_serializer.is_valid():
                profile_serializer.create(request.data)
                return Response(profile_serializer.data)
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
                

            

   
