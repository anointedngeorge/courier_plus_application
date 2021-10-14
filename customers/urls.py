from django.urls import path, re_path
from main.views import (Dashboard, CourierAccountLogin,
 CourierAccountRegister, Homepage)
from . import views
from customers.views import *

app_name = 'customers'

urlpatterns = [
    path('customer/', CustomerView.as_view(), name='customer'),
    path('customerList/', CustomerListView.as_view(), name='customerList'),
    path('customeredit/<int:id>', views.customer_update_form, name='customeredit'),
    path('remove_customer/<int:id>', views.remove_customer, name='remove_customer'),
]