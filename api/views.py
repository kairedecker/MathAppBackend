from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.models import CustomUser
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .permissions import IsGuestUser, IsRegisteredUser

class RegisterGuestUser(APIView):
    ''' 
    Erstellt einen Guest User
    Nutzername und Passwort werden automatisch erzeugt
    Nutername: guestXXXXX
    Passwort: guest
    '''
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
    ''' Gibt die Info des Users zurück - möglich für alle Nutzer'''
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer
    def get(self, request):
        user_name = request.user.user_name
        if CustomUser.objects.filter(user_name=user_name).exists():
            user = CustomUser.objects.get(user_name=user_name)
            serializer = self.serializer_class(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND) 

class UserDelete(APIView):
    ''' User löschen - nur erlaubt für registrierte Nutzer'''
    permission_classes = [IsAuthenticated, IsRegisteredUser]
    erializer_class = CustomUserSerializer
    def delete(self, request):
        user_name = request.user.user_name
        password = request.data['password']
        user = CustomUser.objects.get(user_name=user_name)
        if not user.check_password(password):
            return Response(data={'message': 'Authorization missing'},status=status.HTTP_401_UNAUTHORIZED)
        user.delete()
        return Response(data={'message': 'User deleted'}, status=status.HTTP_202_ACCEPTED)
        
class RegisterUser(APIView):
    ''' Registrieren ist nur für Guest-User möglich '''
    permission_classes = [IsAuthenticated, IsGuestUser]
    serializer_class = RegisterUserSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data, instance=request.user)
        if not CustomUser.objects.filter(user_name=request.user.user_name).exists():
            return Response(data={'message': 'Guest-user not found'},status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(
                    RegisterUserSerializer(user).data,
                    status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

class UpdateUser(APIView):
    ''' Ein Update der User-Daten ist nur für registrierte User möglich '''
    permission_classes = [IsAuthenticated, IsRegisteredUser]
    serializer_class = UpdateUserSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data, instance=request.user)
        if not CustomUser.objects.filter(user_name=request.user.user_name).exists():
            return Response(data={'message': 'User not found'},status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(
                    UpdateUserSerializer(user).data,
                    status=status.HTTP_202_ACCEPTED
                )
        else:
            return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
