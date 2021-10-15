from django import template
from main.models import *
import json
from django.core import serializers

register = template.Library()


@register.simple_tag
def appsettings(fields):
    try:
        settings = GeneralSettings.objects.all()
        
        st = serializers.serialize('python', settings)[0].get('fields')
        return st.get(fields)

    except Exception as e:
        print(e)