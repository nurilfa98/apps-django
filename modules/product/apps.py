from django.apps import AppConfig
from django.db.utils import IntegrityError


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.product'

    def ready(self):
        from .models import Product
        try:
            if not Product.objects.exists():
                Product.objects.bulk_create([
                    Product(name="Mouse Logitech", barcode="P001", price=150000, stock=8),
                    Product(name="Keyboard Mechanical", barcode="P002", price=350000, stock=5)
                ])
        except IntegrityError:
            print("--->> Data already exists.")