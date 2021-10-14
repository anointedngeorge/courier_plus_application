from django.http import request, HttpResponse
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from account.forms import userRegistrationForm
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.conf import settings





def account(request):
    try:
        context = {}
        context['forms'] = userRegistrationForm()
        if request.method == 'POST':
            forms = userRegistrationForm(request.POST)
            if forms.is_valid():
                role_to_group = forms.cleaned_data.get('roles')
                users = forms.save()
                # reapply this rules if you want

                if forms.cleaned_data.get('roles') is not None:
                    permission_group = Group.objects.get(name=f"{role_to_group}")
                    users.groups.add(permission_group)
                
            else:
                messages.error(request, forms.errors)
                forms = userRegistrationForm()
    except:
        pass

    return render(request=request, template_name='extend_registration/create_account.html', context=context)