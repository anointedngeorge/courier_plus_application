from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.http import HttpRequest, request
from django.http.response import HttpResponse
from django.urls import path
from django.shortcuts import render
from account.models import Profile
from containers.models import *
from main.models import *
from django.utils import timezone
from datetime import date
import random
from django.core import serializers







class courierUserDashboard(admin.AdminSite):
    site_header = "Courier Dashboard"
    site_title = "Courier Delivery Service"
    index_title = "Mobis & chennix"
    site_url = 'http://127.0.0.1:8000/'


_dashboard =  courierUserDashboard(name='Mobis Chennix Inventory')




class ContainerDetailsAdminUser(admin.TabularInline):
    model = ContainerDetails
    fields = ['items','size', 'quantity']



class ContainerAdminUser(admin.ModelAdmin):
    search_fields = ['container_ref_startwith',]
    list_display = [
         'user' ,'container_ref', 'weight', 'courier_company',  'destination',
        'country', 'receivers', 'region', 'delivery_status', 'package_type',
        'reason_for_arrival', 'delivery_date', 'assigned', 'created',
    ]
    exclude = ['created', 'updated','package_type', 'reason_for_arrival', 'container_ref', 'receivers','user']
    list_filter = ['container_ref', 'courier_company',]
    list_editable = ['assigned', ]
    inlines = [ContainerDetailsAdminUser]


    def get_queryset(self, request):
        qs = super(ContainerAdminUser, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)
    
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
                    path('printout/', self.printout, name='printout')
                ]
        return new_urls + urls



    def printout(self, request):
        context = {}
        excluded_fields = ['id','user_id', 'created', 'receivers_id', 'reason_for_arrival','package_type', 'assigned','updated']
        fields_container = []
        result_container = []
        # 
        for fields in self.model._meta.fields:
            res = fields.get_attname_column()[0]
            fields_container.append(res)
    

        fields_container_filtered = [fx for fx in fields_container  if not fx in excluded_fields]
        results = self.model.objects.all().filter(user = request.user)
        
        serilized = serializers.serialize('python', results)
        for data in serilized:
            result_container.append(data.get('fields'))

        context['printoutResults'] = result_container
        context['param_fields'] = fields_container_filtered
        return render(request, 'admin/printout.html', context = context)



    def save_model(self, request,  obj, form, change ) -> None:
        randm = random.randint(100, 3000)
        tday = date.today()
        tracking_code = f"MC{obj.region}{tday.day}{tday.month}{tday.year}{randm}"
        obj.user = request.user
        obj.container_ref =  tracking_code
        super().save_model(request, obj, form, change)

_dashboard.register(Container, ContainerAdminUser)



# @admin.register(ContainerTracking)
class ContainerTrackingAdminUser(admin.ModelAdmin):
    pass



class FormChoichAdminUser(admin.ModelAdmin):
    pass

_dashboard.register(FormChoice, FormChoichAdminUser)



# Profile table registered for users
class UsersProfileUsers(admin.ModelAdmin):
    list_display = ['user', 'logo']
    exclude = ['user']
    
    def get_queryset(self, request):
        qs =  super(UsersProfileUsers, self).get_queryset(request)
        
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)
    
    def save_model(self, request, obj, form, change) -> None:
        obj.user = request.user
        super().save_model(request, obj, form, change)


_dashboard.register(Profile, UsersProfileUsers)



# ********************** Model Registration Section **********************
# Profile table registered for the admin
@admin.register(Profile)
class AdminProfileUsers(admin.ModelAdmin):
    list_display = ['user', 'logo']
