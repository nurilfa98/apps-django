"""apps_modular URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from engine.models import Module

urlpatterns = [
    path('admin/', admin.site.urls),
    path('module/', include('engine.urls')),
]

# Tambahkan hanya untuk modul yang sudah diinstall
installed_modules = Module.objects.filter(is_installed=True).values_list("slug", flat=True)
for module in installed_modules:
    urlpatterns.append(path(f"module/{module}/", include(f"modules.{module}.urls")))


# print('-->> url: ', urlpatterns)