from django.contrib import admin
from authModel.models import *

from django.urls import path
from django.shortcuts import render


@admin.register(AppAuthUser)
class AuthModelAdmin(admin.ModelAdmin):
    search_fields = ('username__startwith', )
    list_display = ['first_name', 'last_name','email','is_staff','is_superuser', 'roles']
    list_filter = ['first_name', 'roles', ]

    
    