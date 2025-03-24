from django.urls import path
from . import views

urlpatterns = [
    path('', views.module_list, name='module_list'),
    path('<slug:slug>/', views.module_router, name='module_router'),
    path('apps/install/', views.install_module, name='install_module'),
    path('apps/uninstall/', views.uninstall_module, name='uninstall_module'),
    path('apps/upgrade/<slug:slug>/', views.upgrade_module, name='upgrade_module'),
    path('apps/login/', views.user_login, name='login'),
    path('apps/logout/', views.user_logout, name='logout'),
]