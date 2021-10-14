from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import InstanceCheckMeta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import RegexValidator
from django.utils import timezone
from django_countries.fields import CountryField
from customers.models import *
from employees.models import *
from authModel.models import AppAuthUser
from containers.custom_function import choice


# choice data from custom_function

SHIPMENT_TYPE = choice('SHIPMENT_TYPE')
# BRANCH = [('MAIN','MAIN BRANCH')]
BRANCH = choice('BRANCH')
# PAYMENT_TYPE = [('POSTPAID','Postpaid'), ('PREPAID','Prepaid')]
PACKAGE_TYPE = choice('PACKAGE_TYPE')

RETURN_COST = choice('RETURN_COST') #[('YES', 'Yes'), ('NO','No')]
SHIPMENT_MODE = choice('SHIPMENT_MODE')
# [('20FtTrailer', '20 Ft Trailer'), ('40FtTrailer', '40 Ft Trailer'),
# ('ClosedVan', 'Closed Van'),('ByAir', 'By Air'),('BySea', 'By Sea'),]
    
COURIER_COMPANY =  choice('COURIER_COMPANY') #[('DHL', 'DHL'),('EXPRESS', 'EXPRESS')]
REASONSFORARRIVAL = choice('REASONSFORARRIVAL') #[('UNLOADING', 'UNLOADING'),('CUSTOMSTOP', 'CUSTOM STOP')]
DELIVERY_STATUS = choice('DELIVERY_STATUS') #[('PENDING', 'PENDING'), ('RECEIVED','RECEIVED'),('REJECTED', 'REJECTED')]

ROLES = choice('ROLES') #[('DRIVER', 'DRIVER'),
    # ('MANAGER', 'MANAGER'),]

REGIONS = choice('region')


class Container(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    container_ref = models.CharField(max_length = 150, verbose_name='Tracking Code')
    weight = models.IntegerField(default=0)
    courier_company = models.CharField(choices=COURIER_COMPANY, max_length=50)
    destination = models.CharField(max_length=300)
    country = CountryField(blank_label='(select country)', default="NG")
    receivers   = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True, blank=True)
    region = models.CharField(max_length=100, default='Enugu', choices=REGIONS)
    # container info
    delivery_status = models.CharField(max_length=50, 
    choices= DELIVERY_STATUS)
    package_type = models.CharField(max_length=50, choices=PACKAGE_TYPE)
    reason_for_arrival = models.CharField(max_length=50, choices=REASONSFORARRIVAL)

    delivery_date = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
    assigned  = models.BooleanField(default=0)
    
    updated  = models.DateTimeField(default=timezone.now)
    created  = models.DateTimeField(default=timezone.now)


    class Meta:
        verbose_name_plural = "Container Sheet"

    def __str__(self) -> str:
        return f"{self.container_ref}"

    
    
    

class DateTracker(models.Model):
    registered_date = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
    # container = models.ForeignKey(Container, on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Track Date"

    def __str__(self) -> str:
        return f"{self.registered_date}"


class ContainerDetails(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE, blank=True, null=True)
    items = models.CharField(max_length=50)
    size = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    updated  = models.DateTimeField(default=timezone.now)
    created  = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Container Details"

    def __str__(self) -> str:
        return f"{self.container}"


class ContainerTracking(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name="trackcontainer")
    employee  = models.ForeignKey(AppAuthUser, on_delete=models.CASCADE, blank=True, null=True, related_name="trackemployee",)
    status    = models.IntegerField(blank=True, null=True, default=0)
    location  = models.JSONField(max_length=100, blank=True, null=True, default='')
    accepted  = models.BooleanField(default=0)
    updated   = models.DateTimeField(default=timezone.now)
    created   = models.DateTimeField(default=timezone.now)


    @property
    def get_status_method(self):
        if self.status == 0:
            return "<span class=\"text text-warning\">Pending</span>"
        elif self.status == 1:
            return "<span class=\"text text-success\">Received</span>"
        elif self.status == 2:
            return "<span class=\"text text-danger\">Rejected</span>"







