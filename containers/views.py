from typing import Generator, List

from django.core.checks.messages import Error
from rest_framework import serializers
from django.conf.urls import url
from containers.forms import *
from django.utils import timezone
from django.http import request, HttpResponse
from django.http.response import Http404, JsonResponse
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
from django.views.generic import ListView, DetailView, detail
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from main.error_log_file import MessageWriter
from containers.models import *
from django.views.decorators.csrf import csrf_protect

import json


class ContainerView(ListView):
    model = Container
    allow_empty = True
    template_name = "containers/add_container.html"

    def get(self, *args, **kwargs):
        context = {
            'forms':ContainerForms(),
        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        try:
            if self.request.method == 'POST':
                forms = ContainerForms(self.request.POST)
                if forms.is_valid():
                    # list out the whole item to add
                    items = self.request.POST.getlist('item[]')
                    size = self.request.POST.getlist('size[]')
                    quantity = self.request.POST.getlist('quantity[]')

                    details =  zip(items, size, quantity)
                    container = self.model.objects.all()
                    reference_code = forms.cleaned_data.get('container_ref')
                    if container.filter(container_ref = str(reference_code)).exists() != True:
                        obj = self.model.objects.all()
                        obj = forms.save(commit=False)
                        for item, sizes, qt in details:
                            ContainerDetails.objects.create(
                                items = item,
                                size = sizes,
                                quantity = qt,
                                container_ref = reference_code,
                                # container_id = 1,
                            )
                        obj.save()
                        return redirect('containers:listpackages')
        except Exception as e:
            print(e)
        return redirect('containers:container')
        

# this will be displaying the containers created
class ListContainers(ListView):
    model = Container
    allow_empty = True
    template_name = "containers/list_container.html"

    def get_context_data(self, *args, **kwargs):
        context = {}
        context['detailscontainer'] = ContainerDetails.objects.all()
        context['packages'] = self.model.objects.all()
        return context


def container_update(request, id):
    context = {}
    empl = Container.objects.all().get(pk=id)
    forms = ContainerForms(request.POST or None, instance=empl)
    context['forms'] = forms
    context['containerdata'] = empl
    if request.method == 'POST':
        if forms.is_valid():
            empl = forms.save(commit=False)
            empl.save()
            messages.success(request, 'Updated Successfully')
            return redirect('containers:listpackages')
    return render(request, "containers/container_update_form.html", context)


# remove container + all the items associated to it
def remove_container(request, id):
    code = Container.objects.all().get(id=id)
    details = ContainerDetails.objects.all().filter(container_ref = code.container_ref).delete()
    if details:
        Container.objects.all().filter(pk=id).delete()
    return redirect('containers:listpackages')




def containerDetailedView(request, id):
    context = {}
    context['contdata'] = Container.objects.all().get(pk = id)
    return render(request, "containers/container_detailed_view.html", context)
    

def printoutContainerDetailedView(request, id):
    context = {}
    context['contdata'] = Container.objects.all().get(pk = id)
    return render(request, "containers/printout_container_details.html", context)



def addExtraToContainerRegistered(request, ref):
    try:
        context = {}
        context['ref'] = ref
        context['contdata'] = ContainerDetails.objects.all().filter(container_ref = ref)
        if request.method == 'POST':
            # this items are sent through ajax call in the container_add_more_items.html page.
            # in a json format
            item = request.POST.getlist('item0')[0]
            size = request.POST.getlist('item1')[0]
            quantity = request.POST.getlist('item2')[0]
            id = request.POST.getlist('ID')[0]
            details = ContainerDetails.objects.all().get(id = int(id))
            details.items = item
            details.size = size
            details.quantity = quantity
            details.save()
    except:
        pass
    return render(request, "containers/container_add_more_items.html", context)

# add extra item
def extraDetailsMore(request, ref):
    try:
        containerId = Container.objects.all().get(container_ref = ref)
        if request.method == 'POST':
            items = request.POST.getlist('item[]')
            size = request.POST.getlist('size[]')
            quantity = request.POST.getlist('quantity[]')
            details =  zip(items, size, quantity)
            for item, sizes, qt in details:
                if item !="" and size  != "" and quantity != "":
                    ContainerDetails.objects.create(
                                items = item,
                                size = sizes,
                                quantity = qt,
                                container_ref = ref,
                                # container_id = containerId.id
                            )
                else:
                    print('Empty field not allowed')
        return redirect('containers:listpackages')
    except Exception as e:
        print(e)
    return redirect('containers:listpackages')

def removeItems(request, id):
    ref = request.POST.getlist('ref')[0]
    ContainerDetails.objects.all().filter(pk=id).delete()
    return redirect(f'/extra-details/{ref}')
    


def taskPage(request):
    context = {}
    context['packages'] = Container.objects.all()
    context['employee'] = Employees.objects.all()
    context['tasks'] = ContainerTracking.objects.all()
    return render(request, "containers/list_task.html", context)


def automateTask(request):
    packageid = request.POST.getlist('pkid')[0]
    employeeid = request.POST.getlist('empid')[0]
    tracker = ContainerTracking.objects.all().filter(container_id = packageid, employee_id = employeeid)
    if tracker.exists() == False:
        cont = Container.objects.all().filter(pk = packageid)
        ContainerTracking.objects.create(
                container_id = packageid,
                employee_id = employeeid
            )
        cont.update(assigned = 1)
        return JsonResponse({"status":True}, safe=True)
        
    return JsonResponse({"status":False}, safe=True)

# Remove task assigned to an employee with an ID

def removeTask(request):
    data =  json.loads(request.body)
    taskid = data['taskid']
    
    tracker = ContainerTracking.objects.all().filter(pk = taskid)
    tracker2 = ContainerTracking.objects.all().get(pk = taskid)

    cont = Container.objects.all().filter(pk = tracker2.container.id)
    if tracker.exists() == True:
        tracker.delete()
    cont.update(assigned = 0)
    return JsonResponse({'response':True}, safe=True)


def taskStatus(request):
    data =  json.loads(request.body)
    taskid = data['taskid']
    status = data['status']
    tracker = ContainerTracking.objects.all().filter(pk = taskid)
    if tracker.exists() == True:
        tracker.update(status = status)
    # print(taskid)
    return JsonResponse({'response':True}, safe=True)