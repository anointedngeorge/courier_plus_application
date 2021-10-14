from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from account.admin import _dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('sub-admin/', _dashboard.urls),

    url(r'^media/(?P<path>.*)$', serve,  {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]


admin.site.index_title = "Courier Super Admin"
admin.site.site_header = "Super Administrator"
admin.site.site_title = "Mobis Chennix Ventures"
