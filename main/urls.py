from django.urls import path, re_path
from main.views import (Dashboard, CourierAccountLogin,
 CourierAccountRegister, Homepage)
from . import views
from main.views import *

app_name = 'main'

urlpatterns = []