from django import forms
from django.db.models import fields
from django.db.models.query_utils import Q
from django.forms import widgets
from employees.models import *
from django.contrib.admin.decorators import display
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from authModel.models import AppAuthUser
from django.forms.widgets import CheckboxInput, PasswordInput, ChoiceWidget




class EmployeeForm(forms.ModelForm):
 
    class Meta:
        model = Employees
        fields = ('user','roles')
        widgets = {
            'user':forms.Select(attrs={'class':'form-control', 'placeholder':'Select'}),
            'roles':forms.Select(attrs={'class':'form-control'})
        }
    
    # Get all the users who are the employees = 101
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = AppAuthUser.objects.filter(Q(roles = 'EMPLOYEE'))