from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import RegexValidator
from django.utils import timezone
from django_countries.fields import CountryField
from django.conf import settings


class Customers(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField(default='')
    address = models.CharField(max_length=500, blank=True, null=True, default='')
    states = models.CharField(max_length=100, blank=True, null=True, default='')
    local_government = models.CharField(max_length=100, blank=True, null=True, default='')
    postal_code = models.CharField(max_length=100, blank=True, null=True, default='')
    
    class Meta:
        verbose_name_plural = "Customer sheet"


    def __str__(self) -> str:
        return f"{self.user}"















