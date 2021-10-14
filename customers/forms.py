from django import forms
from django.db.models import fields
from django.forms import widgets
from customers.models import *
from django.contrib.admin.decorators import display
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import CheckboxInput, PasswordInput, ChoiceWidget
from authModel.models import AppAuthUser
from django.db.models.query_utils import Q

class CustomersForm(forms.ModelForm):
 
    class Meta:
        model = Customers
        fields = ('user','phone_number','address', 'states','local_government','postal_code')
        widgets = {
            'user':forms.Select(attrs={'class':'form-control', 'placeholder':'Customer', 'required':True}),
            'phone_number': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'081********','required':True}),
            'address':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address','required':True}),
            'states':forms.TextInput(attrs={'class':'form-control', 'placeholder':'States','required':True}),
            'local_government':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Local Government','required':True}),
            'postal_code':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Postal Code','required':True}),
        }
    

     # Get all the users who are the employees = 101
    def __init__(self, *args, **kwargs):
        super(CustomersForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = AppAuthUser.objects.filter(Q(roles = 'CUSTOMER'))

