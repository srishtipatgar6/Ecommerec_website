from pathlib import Path

from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='mainhome'),

    path('app1/', include('app1.urls')),

    path('__reload__/', include('django_browser_reload.urls')),
]