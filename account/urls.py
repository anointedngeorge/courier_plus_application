from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from account.views import *

app_name = 'account'

urlpatterns = [
    path('account/', account, name="create_account" ),

]

