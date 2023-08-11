from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.models import CustomUser
from .serializers import RegisterCustomUserSerializer
from rest_framework.permissions import IsAuthenticated

class GetRoutes(APIView):
    def get(self, request):
        routes = [
            '/api/login',
            '/api/login/refresh',
            '/api/register',
            '/api/users',
            '/api/delete-user/<str:email>'
        ]
        return Response(routes)
    
class RegisterUser(APIView):
    serializer_class = RegisterCustomUserSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(
                    RegisterCustomUserSerializer(user).data,
                    status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

class UserList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = RegisterCustomUserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class UserDelete(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, email):
        user = CustomUser.objects.get(email=email)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)