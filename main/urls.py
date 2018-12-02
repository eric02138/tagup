"""rest_api URL Configuration
"""
from django.contrib import admin
from django.urls import include, path
from main.views import main_redirect

urlpatterns = [
    path('', main_redirect),
    path('admin/', admin.site.urls),
    path('api/', include('main.api.urls')),
]
