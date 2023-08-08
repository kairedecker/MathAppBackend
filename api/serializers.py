from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'user_name', 'login_provider', 'created_at', 'updated_at']

class RegisterCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password',  'user_name', 'login_provider']
    
    def create(self, validated_data):
        user = CustomUser.objects.create(email=validated_data['email'],
                                         user_name=validated_data['user_name'],
                                         login_provider=validated_data['login_provider']
                                         )
        if validated_data['login_provider'] == 'Mail':
            user.set_password(validated_data['password'])
        user.save()
        return user