from django.http import HttpResponse
from django.http.response import HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect,render, resolve_url
from django.contrib.sites.shortcuts import get_current_site

class CheckUserSiteMiddleware(MiddlewareMixin):
    
     def process_request(self, request):
         user = request.user
         try:
             if user.is_authenticated and user.is_superuser:
                return True
             elif (user.is_authenticated) and not (user.is_superuser) and not (request.path.startswith('/admin/')):
                pass
             elif not user.is_authenticated:
                pass
             else:
                 pass
                #  return HttpResponseForbidden()
                
         except Exception as e:
             return e
