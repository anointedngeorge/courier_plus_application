from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import *


@receiver(post_save, sender=Container)
def post_save_tracking_date(sender, instance, created, *args, **kwargs):
    if created:
        if DateTracker.objects.all().filter(registered_date=timezone.now()).exists():
            pass
        else:
            DateTracker.objects.create(registered_date=timezone.now())