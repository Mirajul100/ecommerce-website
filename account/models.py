from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser

class MyAccountManager(BaseUserManager):

    def create_user(self , first_name , last_name , user_name , email , password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not user_name:
            raise ValueError("User must have an username")
        
        user = self.model(
            
            email = self.normalize_email(email),
            user_name = user_name,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self , first_name , last_name , user_name , email , password):
        user = self.model(
            email = self.normalize_email (email),
            first_name = first_name,
            last_name = last_name,
            user_name = user_name,
            password = password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_super_admin = True  
        user.save(using = self._db)
        return user


class Account(AbstractBaseUser):

    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 50)
    user_name = models.CharField(max_length= 50 , unique= True)
    email = models.EmailField(max_length=100 , unique= True)
    phon_number = models.CharField(max_length= 50)

    date_joining = models.DateTimeField(auto_now_add= True)
    login_date = models.DateField(auto_now= True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["user_name" , "first_name" , "last_name"]

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def perm(self , perm , obj= None):
        return self.is_admin
    
    def hes_module_perms(self ) :
        return True
