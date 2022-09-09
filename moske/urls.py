from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles import views
import django.contrib.auth.urls as auth_urls
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events_registry.urls')),
    path('users/',include('users.urls')),
    path('users/',include(auth_urls)),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', views.serve),
    ]