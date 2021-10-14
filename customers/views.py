from typing import Generator, List

from django.conf.urls import url
from customers.forms import *
from django.utils import timezone
from django.http import request, HttpResponse
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect,render
from django.contrib import messages
from django.contrib.auth.models import User
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
from customers.models import *




# the customer view model function
class CustomerView(ListView):
    model = Customers
    allow_empty = True
    template_name = "customers/add_customer.html"

    def get(self, *args, **kwargs):
        context = {
            'forms':CustomersForm()
        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        forms =  CustomersForm(self.request.POST)
        if forms.is_valid():
            forms.save() 
            
        return redirect('customers:customerList')



class CustomerListView(TemplateView):
    model = Customers
    allow_empty = True
    template_name = "customers/list_customers.html"

    def get_context_data(self, **kwargs):
        context = {}
        context['customers'] = self.model.objects.all()
        return context


# update customers
def customer_update_form(request, id):
    context = {}
    empl = Customers.objects.all().get(pk=id)
    forms = CustomersForm(request.POST or None, instance=empl)

    context['userdata'] = empl
    context['forms'] = forms
    if request.method == 'POST':
        if forms.is_valid():
            empl = forms.save(commit=False)
            empl.save()
            messages.success(request, 'Updated Successfully')
    return render(request, "customers/customer_update_form.html", context)



# remove a customer
def remove_customer(request, id):
    empl = Customers.objects.filter(pk=id).delete()
    # print(id)
    return render(request, "customers/list_employee.html")



