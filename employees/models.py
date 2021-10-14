from django.core import validators
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import RegexValidator
from django.utils import timezone
from django_countries.fields import CountryField

SHIPMENT_TYPE = [('PICKUP','Pickup'),('DROPOFF','Drop Off')]
BRANCH = [('MAIN','MAIN BRANCH')]
PAYMENT_TYPE = [('POSTPAID','Postpaid'), ('PREPAID','Prepaid')]
PACKAGE_TYPE = [('1-10KG','1-10 KG'),('10-20KG','10-20 KG'), 
    ('20-50KG','20-50 KG'),('50-100KG','50-100 KG'), ('100ABOVE','100-ABOVE KG')]
RETURN_COST = [('YES', 'Yes'), ('NO','No')]
SHIPMENT_MODE = [('20FtTrailer', '20 Ft Trailer'), 
        ('40FtTrailer', '40 Ft Trailer'),
        ('ClosedVan', 'Closed Van'),
        ('ByAir', 'By Air'),
        ('BySea', 'By Sea'),
    ]
    
COURIER_COMPANY = [('DHL', 'DHL'),('EXPRESS', 'EXPRESS')]
REASONSFORARRIVAL = [('UNLOADING', 'UNLOADING'),('CUSTOMSTOP', 'CUSTOM STOP')]
DELIVERY_STATUS = [('PENDING', 'PENDING'), ('RECEIVED','RECEIVED'),('REJECTED', 'REJECTED')]

ROLES = [('DRIVER', 'DRIVER'),
    ('MANAGER', 'MANAGER'),]



class Employees(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    roles = models.CharField(max_length=50, choices=ROLES, default='')

    class Meta:
        verbose_name_plural = "Employee Sheet"

    def __str__(self) -> str:
        return f"{self.user}"
    


    
    




