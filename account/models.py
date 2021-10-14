from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from authModel.models import AppAuthUser



class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
     related_name="profile")
    logo = models.ImageField(upload_to='logos', max_length=100, blank=True, null=True, 
    verbose_name="Profile logo")
    

    class Meta:
        verbose_name_plural = "Profile Settings"
        

    def __str__(self) -> str:
        return f"{self.user}"