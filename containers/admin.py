from django.contrib import admin
from .models import *
from datetime import date
from django.urls import path
from django.shortcuts import render
import random
from django.core import serializers



class ContainerDetailsAdmin(admin.TabularInline):
    model = ContainerDetails
    fields = ['items','size', 'quantity']



@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    search_fields = ['container_ref_startwith',]
    list_display = [
        'user','container_ref', 'weight', 'courier_company', 'destination',
        'country', 'receivers', 'region', 'delivery_status', 'package_type',
        'reason_for_arrival', 'delivery_date', 'assigned', 'created',
    ]
    exclude = ['created', 'updated','package_type', 'reason_for_arrival', 'container_ref', 'receivers']
    list_filter = ['container_ref', 'courier_company',]
    inlines = [ContainerDetailsAdmin]


    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
                    path('printout/', self.printout, name='printout')
                ]
        return new_urls + urls



    def printout(self, request):
        context = {}
        excluded_fields = ['id','user_id', 'receivers_id', 'reason_for_arrival','package_type','assigned','updated']
        fields_container = []
        result_container = []
        for fields in self.model._meta.fields:
            res = fields.get_attname_column()[0]
            fields_container.append(res)
    

        fields_container_filtered = [fx for fx in fields_container  if not fx in excluded_fields]
        results = self.model.objects.all()
        
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
        obj.container_ref =  tracking_code
        super().save_model(request, obj, form, change)


@admin.register(ContainerTracking)
class ContainerTrackingAdmin(admin.ModelAdmin):
    pass