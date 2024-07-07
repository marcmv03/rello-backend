from django.shortcuts import render

# Create your views here.
# board/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Profile
from rest_framework import serializers

from profile.serializers import ProfileSerializer
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
            if profile.id !=  request.user :
                return Response({"error":"You are not the user of this profile"},status =status.HTTP_401_UNAUTHORIZED )
            profile_serializer = ProfileSerializer(profile,data=request.data)
            if profile_serializer.is_valid():
                profile_serializer.update(profile,request.data)
                return Response(profile_serializer.data)
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
              
class ProfileCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self,request,format=None):
        try :
            profile_serializer = ProfileSerializer(data=request.data)
            if profile_serializer.is_valid():
                id = profile_serializer.create(request.data)
                if id :
                    return Response({"id": id}, status=status.HTTP_201_CREATED)
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
      
                

            

   
