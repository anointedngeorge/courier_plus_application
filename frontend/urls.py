from django.urls import path, re_path
from . import views
from .views import *

app_name = 'frontend'

urlpatterns = [
    path('', views.index, name='frontpage'),
]