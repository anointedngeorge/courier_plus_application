from django.urls import path, re_path
from . import views
from employees.views import *

app_name = 'employees'

urlpatterns = [
    path('employee/', EmployeeView.as_view(), name='employee'),
    path('employeeList/', EmployeeListView.as_view(), name='employeeList'),
    path('edit/<int:id>', views.employee_update_form, name='edit'),
    path('remove_employee/<int:id>', views.remove_employee, name='remove_employee'),
]