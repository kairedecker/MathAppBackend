from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random
import string

GUEST_PASSWORD = 'guest'
GUEST_USER_SUFIX_LENGTH = 5
GUEST_USER_PREFIX = "guest#"

class CustomUserManager(BaseUserManager):

    def _generate_guest_username():
        while True:
            generated_guest_username_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=GUEST_USER_SUFIX_LENGTH))
            if not CustomUser.objects.filter(user_name=GUEST_USER_PREFIX+generated_guest_username_suffix).exists():
                break
        return GUEST_USER_PREFIX + generated_guest_username_suffix
      
    def create_guest_user(self, **extra_fields):
        is_guest = True
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        generated_guest_username = CustomUserManager._generate_guest_username()
        user = self.model(is_guest=is_guest, user_name=generated_guest_username, **extra_fields)
        user.set_password(GUEST_PASSWORD)
        return user

    def create_superuser(self, email, password, **extra_fields):
        # Create and save a SuperUser with the given email and password.
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        login_provider = "Mail"
        if extra_fields.get("is_staff") is not True:
            raise ValueError(("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))
        return self._create_user(email, login_provider, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=30, unique=True, blank=True, null=True)
    email = models.EmailField(db_index=True, max_length=255,  unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    login_provider = models.CharField(max_length=10)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_name'
    #REQUIRED_FIELDS = ['user_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.user_name
    