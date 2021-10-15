
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin,
    BaseUserManager
)

from django.contrib.sites.models import Site
# this is my defined custom extra py file, to fetch all the groups defined
from authModel.extra import group_to_roles
# Create your models here.

ROLES = group_to_roles()


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, first_name=None, last_name=None, email=None, password=None, **other_fields):
        try:    
            other_fields.setdefault('is_active', True)
            other_fields.setdefault('is_staff', True)
            other_fields.setdefault('is_superuser', True)
            
            if other_fields.get('is_staff') is not True:
                raise ValueError(
                    'Super user must be assigned to is_staff=True' )
            if other_fields.get('is_superuser') is not True:
                raise ValueError(
                    'Super user must be assigned to is_superuser=True' )
            
            return self.create_user(first_name, last_name , email, password, **other_fields)
        except Exception as er:
            return er
    
    def create_user(self, first_name=None ,last_name=None , email=None, password=None, roles=None, **other_fields):
        try:  
            if not email:
                raise ValueError(_('You must provide an email address!'))
            email = self.normalize_email(email)
            user = self.model(first_name=first_name, last_name=last_name, email=email, roles = roles, **other_fields)
            user.set_password(password)
            user.save()
            return user
        except Exception as er:
            return er
        
    
    
    
class AppAuthUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(_('email_address'), unique=True)
    username = models.CharField(max_length=300, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    site = models.ForeignKey(Site, null=True, on_delete=models.CASCADE)
    roles = models.CharField(choices=ROLES, default='', max_length=300, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name',]


    class Meta:
        verbose_name_plural = "Authentication"
    
    

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"



    
