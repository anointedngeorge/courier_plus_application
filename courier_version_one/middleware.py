from django.http import HttpResponseForbidden
from django.contrib.sites.shortcuts import get_current_site


class CheckUserSiteMiddleware(object):

    def process_request(self, request):
        user = request.user
        if (request.path.startswith('/admin/') and
                request.user.is_authenticated() and
                user.site != get_current_site()):
            return HttpResponseForbidden()