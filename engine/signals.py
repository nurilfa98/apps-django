from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from django.urls import clear_url_caches, path, include
from django.conf import settings
from engine.models import Module
import importlib


@receiver(post_save, sender=Module)
def reload_urls_on_module_save(sender, instance, **kwargs):
    """
    Reload urlpatterns when a Module is saved
    """
    clear_url_caches()

    # Import ROOT_URLCONF sebagai modul Python
    urls_module = importlib.import_module(settings.ROOT_URLCONF)

    # Update urlpatterns
    installed_modules = Module.objects.filter(is_installed=True).values_list("slug", flat=True)

    new_urlpatterns = [
        path('admin/', admin.site.urls),
        path('module/', include('engine.urls')),
    ]

    for module in installed_modules:
        new_urlpatterns.append(path(f"module/{module}/", include(f"modules.{module}.urls")))

    # Set ulang urlpatterns
    urls_module.urlpatterns = new_urlpatterns
    print("--->> [URL RELOAD] URLs updated after module save")
