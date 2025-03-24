from django.apps import AppConfig
from django.db.utils import IntegrityError


class EngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'engine'

    def ready(self):
        import engine.signals
        from .models import Module, Permission
        try:
            if not Module.objects.exists():
                Module.objects.create(name="Product", slug="product", is_installed=False)
            if not Permission.objects.exists():
                Permission.objects.bulk_create([
                    Permission(role="manager", is_create=True, is_read=True, is_update=True, is_delete=True),
                    Permission(role="user", is_create=True, is_read=True, is_update=True, is_delete=False),
                ])
        except IntegrityError:
            print("--->> Data already exists.")