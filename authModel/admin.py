from django.contrib import admin
from django.contrib.admin.sites import site
from authModel.models import *

from django.urls import path
from django.shortcuts import render


@admin.register(AppAuthUser)
class AuthModelAdmin(admin.ModelAdmin):
    search_fields = ('username__startwith', )
    list_display = ['first_name', 'last_name','email','is_staff','is_superuser', 'roles']
    list_filter = ['first_name', 'roles', ]


    def save_model(self, request, obj, form, change) -> None:
        if len(obj.password) > 70:
            pass
        else:
            obj.set_password(obj.password)
        obj.is_active = True
        return super().save_model(request, obj, form, change)

    


    

    
    
