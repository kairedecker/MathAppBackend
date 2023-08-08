from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, user_name, login_provider, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not user_name:
            raise ValueError('Users must have a user name')
        user = self.model(
            email=self.normalize_email(email),
            user_name=user_name,
            **extra_fields
        )
        if(login_provider != None):
            if login_provider == "Mail":
                user.login_provider = login_provider
                user.set_password(password)
            else:
                user.login_provider = login_provider
            user.save(using=self._db)
            return user
        else:
            raise ValueError('Users must have a login provider')
    
    def create_user(self, email, user_name, login_provider, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, user_name, login_provider, password, **extra_fields)

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
    user_name = models.CharField(max_length=30, unique=True)
    email = models.EmailField(db_index=True, max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #last_login = models.DateTimeField()
    login_provider = models.CharField(max_length=10)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIERED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.email