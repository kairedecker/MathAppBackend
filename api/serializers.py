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
        fields = ['id', 'is_guest', 'user_name']
        extra_kwargs = {'user_name': {'read_only': True}}

    
    def create(self, validated_data):
        print(validated_data)
        user = CustomUser.objects.create_user(
                                        is_guest=validated_data['is_guest'],
                                        )
        user.save()
        return user

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'is_guest', 'user_name', 'email', 'password', 'login_provider']
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate_user_name(self, value):
        if CustomUser.objects.filter(user_name=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError('Username already exists')
        return value

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.login_provider = validated_data.get('login_provider', instance.login_provider)
        instance.is_guest = validated_data.get('is_guest', instance.is_guest)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance
    

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'user_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate_user_name(self, value):
        if CustomUser.objects.filter(user_name=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError('Username already exists')
        return value

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance
