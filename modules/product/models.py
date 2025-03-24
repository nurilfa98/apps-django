from django.db import models
import uuid


class Product(models.Model):
    id       = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name     = models.CharField(max_length=100)
    barcode  = models.CharField(max_length=100, unique=True)
    price    = models.DecimalField(max_digits=10, decimal_places=2)
    stock    = models.IntegerField()

    # untuk testing fitur upgrade module
    # description = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'product'