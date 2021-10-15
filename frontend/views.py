from typing import Generator, Iterable, List
from django.conf.urls import url
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


# creating Employee detailed section
def index(request):
    return render(request, "frontend/index.html")





