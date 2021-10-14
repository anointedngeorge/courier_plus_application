from typing import Generator, Iterable, List
from django.conf.urls import url
from django.forms.formsets import formset_factory
from employees.forms import *
from django.utils import timezone
from django.http import request, HttpResponse
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect,render
from django.contrib import messages
from django.contrib.auth.models import User
from authModel.models import AppAuthUser # new app authentication user model
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
from employees.models import *


# creating Employee detailed section
class EmployeeView(ListView):
    model = Employees
    allow_empty = True
    template_name = "employees/add_employee.html"

    def get(self, *args, **kwargs):
        forms =EmployeeForm()
        context = {
            'forms':forms
        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        forms =  EmployeeForm(self.request.POST)
        if forms.is_valid():
            employee = self.model.objects.create(
                    user = forms.cleaned_data.get('user'),
                    roles = forms.cleaned_data.get('roles')
            )
        return redirect('employees:employeeList')


class EmployeeListView(TemplateView):
    model = Employees
    allow_empty = True
    template_name = "employees/list_employee.html"

    def get_context_data(self, **kwargs):
        context = {}
        context['employees'] = self.model.objects.all()
        return context


def employee_update_form(request, id):
    context = {}
    empl = Employees.objects.all().get(pk=id)
    forms = EmployeeForm(request.POST or None, instance=empl)

    context['userdata'] = empl
    context['forms'] = forms
    if request.method == 'POST':
        if forms.is_valid():
            empl = forms.save(commit=False)
            empl.save()
            messages.success(request, 'Updated Successfully')
            return redirect('employees:employeeList')
    return render(request, "employees/employee_update_form.html", context)
    

def remove_employee(request, id):
    empl = Employees.objects.filter(pk=id).delete()
    # print(id)
    return render(request, "employees/list_employee.html")








