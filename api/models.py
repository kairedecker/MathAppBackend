from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random
import string

class CustomUserManager(BaseUserManager):

    def _generate_guest_username():
        length = 5
        while True:
            generated_guest_username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            if not CustomUser.objects.filter(user_name=generated_guest_username).exists():
                break
        return 'guest' + generated_guest_username
      
    def create_guest_user(self, is_guest, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        generated_guest_username = CustomUserManager._generate_guest_username()
        print(generated_guest_username)
        user = self.model(is_guest=is_guest, user_name=generated_guest_username, **extra_fields)
        user.set_password('guest')
        return user 

    def create_superuser(self, email, password, **extra_fields):
        # Create and save a SuperUser with the given email and password.
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        login_provider = "Mail"
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self._create_user(email, login_provider, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=30, unique=True, blank=True, null=True)
    email = models.EmailField(db_index=True, max_length=255,  unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #last_login = models.DateTimeField()
    login_provider = models.CharField(max_length=10)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_name'
    REQUIERED_FIELDS = ['user_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.user_name
    