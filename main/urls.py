from django.urls import path, re_path
from main.views import (Dashboard, CourierAccountLogin,
 CourierAccountRegister, Homepage)
from . import views
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('login/', CourierAccountLogin.as_view(), name='account_login'),
    path('register/', CourierAccountRegister.as_view(), name='register'),
    path('logout/', views.logout_user, name='account_logout'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('appsettings/', views.appSettings, name='appsettings'),
    path('settingspage/<str:pagename>', views.settingsPage, name='settingspage'),
    path('remove-regitered-choice/<int:id>', views.removeRegiteredRchoice, name='remove-regitered-choice'),


    # frontpage
    path('page/<str:pagename>', views.sitepages, name='sitepage'),




   

]