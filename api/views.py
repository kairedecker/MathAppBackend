from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.models import CustomUser
from .serializers import RegisterGuestSerializer, CustomUserSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsGuestUser

class RegisterGuestUser(APIView):
    serializer_class = RegisterGuestSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(
                    RegisterGuestSerializer(user).data,
                    status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

class UserInfo(APIView):
    permission_classes = [IsAuthenticated, IsGuestUser]
    serializer_class = CustomUserSerializer
    def get(self, request, user_name):
        if CustomUser.objects.filter(user_name=user_name).exists():
            user = CustomUser.objects.get(user_name=user_name)
            serializer = self.serializer_class(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND) 

class UserDelete(APIView):
    permission_classes = [IsAuthenticated]
    erializer_class = CustomUserSerializer
    def delete(self, request, user_name):
        try:
            user = CustomUser.objects.get(user_name=user_name)
            user.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)