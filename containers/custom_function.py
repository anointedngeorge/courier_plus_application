from main.models import *
from django.core import serializers as ser
import time

def choice(selectors):
    try:
        container = []
        sel = FormChoice.objects.all().filter(selector = str(selectors).upper())
        for selector in sel:
            ff = (f'{selector.code}',f'{selector.name}')
            container.append(ff)
        return container

    except:
        pass
