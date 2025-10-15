from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, user_name, email, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not user_name:
            raise ValueError("User must have a username")
        
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            user_name=user_name,
        )

        user.set_password(password)
        user.is_active = True  # Ensure users are active by default
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, user_name, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            user_name=user_name,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True  # Use is_superuser from PermissionsMixin
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    user_name       = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50)  # Fixed typo

    date_joined     = models.DateTimeField(auto_now_add=True)  # Renamed for convention
    last_login      = models.DateTimeField(auto_now=True)  # Changed to DateTimeField
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)  # Replaced is_super_admin

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin  # Simplified; can be expanded with PermissionsMixin
    
    def has_module_perms(self, app_label):
        return True  # Simplified; can be expanded with PermissionsMixin