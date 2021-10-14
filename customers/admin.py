from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    pass



