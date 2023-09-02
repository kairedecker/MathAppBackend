from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'user_name', 'login_provider', 'created_at', 'updated_at', 'is_guest']

class RegisterGuestSerializer(serializers.ModelSerializer):
    '''
    Der User als Guest-User erstellt
    is_guest wird dabei automatisch auf True gesetzt
    Der Nutzername wird automatisch im Model generiert -> siehe models.py
    '''
    class Meta:
        model = CustomUser
        fields = ['id', 'is_guest', 'user_name']
        extra_kwargs = {
            'user_name': {'read_only': True},
            'is_guest': {'read_only': True}
        }
    
    def create(self, validated_data):
        user = CustomUser.objects.create_guest_user()
        user.save()
        return user

class RegisterUserSerializer(serializers.ModelSerializer):
    ''' 
    Der User wird geupdated und Setzt notwendige Daten für die Registrierung 
    is_guest wird dabei automatisch auf False gesetzt
    Wird is_guest im Body gesendet, wird dies ignoriert!
    '''
    class Meta:
        model = CustomUser
        fields = ['id', 'is_guest', 'user_name', 'email', 'password', 'login_provider']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_guest': {'read_only': True}
        }
    
    def validate_email(self, value):
        '''
        Validierung der Email unter Ausschluss des eigenen Users
        '''
        if CustomUser.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate_user_name(self, value):
        '''
        Validierung des Usernames unter Ausschluss des eigenen Users
        '''
        if CustomUser.objects.filter(user_name=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError('Username already exists')
        return value

    def update(self, instance, validated_data):
        is_guest = False
        instance.email = validated_data.get('email', instance.email)
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.login_provider = validated_data.get('login_provider', instance.login_provider)
        instance.is_guest = is_guest
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
