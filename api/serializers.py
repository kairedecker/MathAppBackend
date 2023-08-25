from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import random
import string

DIGIT_COUNT = 5

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'user_name', 'login_provider', 'created_at', 'updated_at', 'is_guest']

class RegisterGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'is_guest', ]
        extra_kwargs = {'user_name': {'read_only': True}}

    
    def create(self, validated_data):
        print(validated_data)
        user = CustomUser.objects.create_user(
                                        is_guest=validated_data['is_guest'],
                                        )
        user.save()
        return user