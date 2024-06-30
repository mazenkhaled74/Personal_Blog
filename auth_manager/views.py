from django.shortcuts import render
from rest_framework.views import APIView
from auth_manager.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            hashed_password = make_password(password)
            serializer.validated_data['password'] = hashed_password

            serializer.save()
            print("User is here")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogInView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Password and Username are required'})
        
        user = authenticate(username=username, password=password)

        if user is not None:
            return Response("Loged in successfully", status=status.HTTP_200_OK)
        else:
            return Response("Invalid Credentials", status=status.HTTP_401_UNAUTHORIZED)