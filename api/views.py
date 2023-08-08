from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegisterCustomUserSerializer

class GetRoutes(APIView):
    def get(self, request):
        routes = [
            '/api/token',
            '/api/token/refresh',
        ]
        return Response(routes)
    
class RegisterUser(APIView):
    serializer_class = RegisterCustomUserSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
                RegisterCustomUserSerializer(user).data,
                status=status.HTTP_201_CREATED
            )
        

