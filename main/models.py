
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import RegexValidator
from django.utils import timezone
from django_countries.fields import CountryField
from main.timezones import timezones_region
from django.contrib.auth.models import AbstractUser
from django.db import models


LANGUAGE = [('ENG', 'English Language'),('SPANISH', 'Spanish'), ('FRENCH', 'French'), ]
THEME = [('DARK','Dark'),('LIGHT','Light'),('CLASSIC','Classic')]
THEME_COLOUR = [('RED','Red'), ('GRAY', 'Gray')]
FONT_SIZE = [(i,i) for i in range(1,20)]

EMAIL_SECURITY = [('TLS','TLS'), ('SSL','SSL'), ('False','False')]

TIMEZONES = timezones_region


FORMCHOICE = [
    ('REGION', 'REGION'),
    ('PACKAGE_TYPE', 'PACKAGE TYPE'),
    ('COURIER_COMPANY', 'COURIER COMPANY'),
    ('DELIVERY_STATUS', 'DELIVERY STATUS'),
    ('REASONSFORARRIVAL', 'REASONS FOR ARRIVAL'),
    ('SHIPMENT_TYPE', 'SHIPMENT TYPE'),
    ('BRANCH', 'BRANCH'),
    ('RETURN_COST', 'RETURN COST'),
    ('PAYMENT_TYPE', 'PAYMENT TYPE'),
    ('ROLES', 'ROLES'),
]


class GeneralSettings(models.Model):

    site_title = models.CharField(max_length=100, blank=True, null=True, default='')
    site_descriptions = models.TextField(max_length=200, blank=True, null=True, default='Site Descriptions')
    site_logo =  models.FileField(upload_to='settings', blank=True, null=True, default='')
    site_favicon =  models.FileField(upload_to='settings', blank=True, null=True, default='')
    google_analytics  = models.CharField(max_length=100, blank=True, null=True, default='')


    class Meta:
        verbose_name_plural = "General Settings"

    def __str__(self) -> str:
        return f'{self.site_title}'


class SystemSettings(models.Model):

    langauge = models.CharField(choices=LANGUAGE, max_length=100, blank=True, null=True, default='Select')
    timezone = models.CharField(blank=True, null=True, choices=TIMEZONES, max_length=100)
    ip_restrictions  = models.TextField(max_length = 150, blank=True, null=True)

    class Meta:
        verbose_name_plural = "System Settings"

    def __str__(self) -> str:
        return f'{self.langauge}'


class EmailSettings(models.Model):

    protocol = models.CharField(max_length=100, blank=True, null=True, default='')
    smtp_host = models.CharField(max_length=100, blank=True)
    smtp_username  = models.CharField(max_length = 150, blank=True)
    smtp_security  = models.CharField(choices=EMAIL_SECURITY, max_length = 150, blank=True)
    smtp_port  = models.IntegerField(blank=True, null=True)
    smtp_password  = models.CharField(max_length = 150, blank=True)

    class Meta:
        verbose_name_plural = "Email Settings"

    def __str__(self) -> str:
        return f'{self.smtp_host}'



class ThemeSettings(models.Model):
     
    theme = models.CharField(choices=THEME, max_length=100, blank=True, null=True, default='')
    theme_colour = models.CharField(choices=THEME_COLOUR, max_length=100, blank=True)
    font_size  = models.CharField(choices=FONT_SIZE, max_length = 150, blank=True)

    class Meta:
        verbose_name_plural = "Theme Settings"

    def __str__(self) -> str:
        return f'{self.theme}'



class FormChoice(models.Model):
     selector = models.CharField(max_length=100, blank=True, null=True, choices=FORMCHOICE)
     name = models.CharField(max_length=100, blank=True, null=True)
     code = models.CharField(max_length=100, blank=True, null=True)

    
     class Meta:
        verbose_name_plural = "Parameter Tags"

     def __str__(self) -> str:
        return f'{self.selector}'