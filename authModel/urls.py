from django.urls import path, re_path
from authModel import views

app_name = 'authModel'

urlpatterns = [
    path('createusers/', views.createusers, name='createusers'),
]