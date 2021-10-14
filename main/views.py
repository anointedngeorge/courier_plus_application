from typing import Generator, List
from django.core import serializers
from django.conf.urls import url
from django.http import response
from main.forms import *
from django.utils import timezone
from django.http import request, HttpResponse
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect,render
from django.contrib import messages
from authModel.models import AppAuthUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model

from django.views.generic.base import TemplateResponseMixin, TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from main.error_log_file import MessageWriter
from main.models import *
from courier.settings_from_db import AppSettings

from containers.models import ContainerTracking

THEME = "logistics"

class Homepage(ListView):
    model = AppAuthUser    
    allow_empty = True
    template_name = f"base_frontend/{THEME}/index.html"



def sitepages(request, pagename):
    
    return render(request, f"base_frontend/{THEME}/{pagename}.html")



class CourierAccountLogin(TemplateView):
    model = AppAuthUser    
    allow_empty = True
    template_name = "base_templates/login.html"
    
    def post(self, *args, **kwargs):
        try:
            user =  self.request.POST.get('username')
            passw =  self.request.POST.get('password')
            users = authenticate(username=user, password=passw)
            login(self.request, users)
            if self.request.user.is_authenticated:
                return redirect('main:dashboard' )
            else:
                return redirect('main:account_login' )
        except Exception as e:
            """
                Write into a error into a log file
            """
            error_message = f'Error: {e} - from {__class__} Time: {timezone.now()} \n'
            message_writer = MessageWriter('log.txt', 'a')
            with message_writer.open_file() as my_file:
                my_file.write(error_message)

        return HttpResponse('Account Post Method')




def logout_user(request):
    logout(request)
    result = "You have successfully logged out."
    messages.info(request, result)
    return redirect('main:account_login')



class CourierAccountRegister(TemplateView):
    model = AppAuthUser    
    allow_empty = True
    template_name = "base_templates/signup.html"


class Dashboard(ListView):
    model = AppAuthUser
    allow_empty = True
    template_name = "base_templates/index.html"
    
    def get_context_data(self, **kwargs):
        context = {}
        context['tasks'] = ContainerTracking.objects.all()
        AppSettings().settingsData()
        return context
    
    
def appSettings(request):
    context = {}
    return render(request, 'base_templates/settings.html', context)

# load settings pages via jquery from the settings file 
def settingsPage(request, pagename):
    if pagename == 'general_settings':
        context = {}
        formss = GeneralSettings.objects.all()
        
        if len(formss) > 0:
            update_form = GeneralSettingsForms(request.POST or None,  instance= formss[0])
            context['forms'] = update_form
        else:
            context['forms'] = GeneralSettingsForms()

        if request.method == 'POST':
            forms = GeneralSettingsForms(request.POST, request.FILES, instance= formss[0])
            
            if len(formss) == 0 and forms.is_valid():
                forms.save()
                return redirect('main:appsettings')
            else:
                if forms.is_valid():
                    update_forms = GeneralSettingsForms(request.POST, request.FILES, instance= formss[0])
                    update_forms.save()
                    return redirect('main:appsettings')
                
        return render(request, f'base_templates/{pagename}.html' , context)
    
    
    elif pagename == 'system_settings':
        context = {}
        formss = SystemSettings.objects.all()
        
        if len(formss) > 0:
            update_form = SystemSettingsForms(request.POST or None, instance= formss[0])
            context['forms'] = update_form
        else:
            context['forms'] = SystemSettingsForms()

        if request.method == 'POST':
            forms = SystemSettingsForms(request.POST, request.FILES)
            if len(formss) == 0 and forms.is_valid():
                forms.save()
                return redirect('main:appsettings')
            else:
                if forms.is_valid():
                    update_form = SystemSettingsForms(request.POST or None, instance= formss[0])
                    update_form.save()
                    return redirect('main:appsettings')

        return render(request, f'base_templates/{pagename}.html', context)



    elif pagename == 'choice_settings':
        context = {}
        formss = FormChoice.objects.all()
        context['forms'] = FormChoicForm()
        context['options'] = formss

        if request.method == 'POST':
            forms = FormChoicForm(request.POST)
            forms.save()
            return redirect('main:appsettings')

        return render(request, f'base_templates/{pagename}.html', context)

    elif pagename == 'email_settings':
        context = {}
        formss = EmailSettings.objects.all()
        
        if len(formss) > 0:
            update_form = EmailSettingsForms(request.POST or None, instance= formss[0])
            context['forms'] = update_form
        else:
            context['forms'] = EmailSettingsForms()

        if request.method == 'POST':
            forms = EmailSettingsForms(request.POST, request.FILES)
            if len(formss) == 0 and forms.is_valid():
                forms.save()
                return redirect('main:appsettings')
            else:
                if forms.is_valid():
                    update_form = EmailSettingsForms(request.POST or None, instance= formss[0])
                    update_form.save()
                    return redirect('main:appsettings')
        return render(request, f'base_templates/{pagename}.html', context)
    
    elif pagename == 'appearance_settings':
        context = {}
        formss = ThemeSettings.objects.all()
        
        if len(formss) > 0:
            update_form = ThemeSettingsForms(request.POST or None, instance= formss[0])
            context['forms'] = update_form
        else:
            context['forms'] = ThemeSettingsForms()

        if request.method == 'POST':
            forms = ThemeSettingsForms(request.POST, request.FILES)
            if len(formss) == 0 and forms.is_valid():
                forms.save()
                return redirect('main:appsettings')
            else:
                if forms.is_valid():
                    update_form = ThemeSettingsForms(request.POST or None, instance= formss[0])
                    update_form.save()
                    return redirect('main:appsettings')
    # 
    return render(request, f'base_templates/{pagename}.html' )


# add a new employee
def removeRegiteredRchoice(request, id):
    FormChoice.objects.all().filter(pk = id).delete()
    return redirect('main:appsettings')

    


