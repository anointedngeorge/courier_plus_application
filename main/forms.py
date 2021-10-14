from authModel.models import AppAuthUser
from django import forms
from django.db.models import fields
from django.forms import widgets
from main.models import *
from django.contrib.admin.decorators import display
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import CheckboxInput, PasswordInput, ChoiceWidget



class GeneralSettingsForms(forms.ModelForm):
    class Meta:
        model = GeneralSettings
        fields = ['site_title', 'site_descriptions', 'site_logo', 'site_favicon', 'google_analytics']
        widgets = {
            'site_title' : forms.TextInput(attrs = {'placeholder':'Enter Site Title', 'class':'form-control'}),
            'site_descriptions' : forms.Textarea(attrs = {'class':'form-control', 'height':100}),
            'site_logo' : forms.FileInput(attrs = {'class':'form-control'}),
            'site_favicon' : forms.FileInput(attrs = {'class':'form-control'}),
            'google_analytics' : forms.Textarea(attrs = {'class':'form-control', 'height':150}),
        }



class SystemSettingsForms(forms.ModelForm):
    class Meta:
        model = SystemSettings
        fields = ['langauge', 'timezone', 'ip_restrictions']
        widgets = {
            'langauge' : forms.Select(attrs = {'placeholder':'Enter Site Title', 'class':'form-control'}),
            'timezone' : forms.Select(attrs = {'class':'form-control'}),
            'ip_restrictions' : forms.Textarea(attrs = {'placeholder':'Enter ip address you want to block with a comma. ', 'class':'form-control', 'height':100,'required':False}),
        }


class EmailSettingsForms(forms.ModelForm):
    class Meta:
        model = EmailSettings
        fields = ['protocol', 'smtp_host', 'smtp_username','smtp_security','smtp_port','smtp_password']
        widgets = {
            'protocol' : forms.TextInput(attrs = {'placeholder':'Email Backend Protocol Server', 'class':'form-control'}),
            'smtp_host' : forms.TextInput(attrs = {'class':'form-control'}),
            'smtp_username' : forms.TextInput(attrs = {'class':'form-control'}),
            'smtp_security' : forms.Select(attrs = {'class':'form-control'}),
            'smtp_port' : forms.NumberInput(attrs = {'class':'form-control'}),
            'smtp_password' : forms.TextInput(attrs = {'class':'form-control', 'type':'password' }),
            
        }



# appearance settings form
class ThemeSettingsForms(forms.ModelForm):
    class Meta:
        model = ThemeSettings
        fields = ['theme', 'theme_colour', 'font_size']
        widgets = {
            'theme' : forms.Select(attrs = {'placeholder':'Choose Theme', 'class':'form-control'}),
            'theme_colour' : forms.Select(attrs = {'class':'form-control'}),
            'font_size' : forms.Select(attrs = {'class':'form-control'}),
        }


class FormChoicForm(forms.ModelForm):
    class Meta:
        model = FormChoice
        fields = ['selector', 'name','code']
        widgets = {
            'selector' : forms.Select(attrs = {'placeholder':'Select', 'class':'form-control','required':True}),
            'name' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Required name', 'required':True}),
            'code' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Required Code', 'required':True}),
            
        }