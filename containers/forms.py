from django import forms
from django.db.models import fields
from django.db.models.query_utils import Q
from django.forms import widgets
from containers.models import *
from django.contrib.admin.decorators import display
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import CheckboxInput, PasswordInput, ChoiceWidget

class ContainerForms(forms.ModelForm):
 
    class Meta:
        model = Container
       
        fields = ('container_ref', 'weight','courier_company','destination','country', 'region','delivery_status','package_type','reason_for_arrival','receivers')
       
        widgets = {
            'container_ref':forms.TextInput(attrs={'class':'form-control','placeholder':'tracking code','readonly':True}),
            # 'size':forms.NumberInput(attrs={'class':'form-control'}),
            # 'quantity':forms.NumberInput(attrs={'class':'form-control'}),
            'weight':forms.NumberInput(attrs={'class':'form-control'}),
            'destination':forms.TextInput(attrs={'class':'form-control','placeholder':'destination'}),
            'region':forms.Select(attrs={'class':'form-control','placeholder':'Address'}),
            # 'item_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name of container'}),
            'delivery_status':forms.Select(attrs={'class':'form-control'}),
            'receivers':forms.Select(attrs={'class':'form-control'}),
            'reason_for_arrival':forms.Select(attrs={'class':'form-control'}),
            'package_type':forms.Select(attrs={'class':'form-control'}),
            'country':forms.Select(attrs={'class':'form-control'}),
            'courier_company':forms.Select(attrs={'class':'form-control'}),
            'delivery_status':forms.Select(attrs={'class':'form-control'}),
        }




class ContainerdetailsForms(forms.ModelForm):
 
    class Meta:
        model = ContainerDetails
        fields = ('container_ref', 'size','quantity','items')
       
        widgets = {
            'container_ref':forms.TextInput(attrs={'class':'form-control','placeholder':'tracking code','readonly':True}),
            'size':forms.NumberInput(attrs={'class':'form-control'}),
            'quantity':forms.NumberInput(attrs={'class':'form-control'}),
            'items':forms.TextInput(attrs={'class':'form-control','placeholder':'Name of container'}),
            
        }


    # def __init__(self, *args, **kwargs):
    #     super(ContainerdetailsForms, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         print(field)