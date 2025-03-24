from django.db import models
from django.utils.text import slugify
import uuid


class Module(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name          = models.CharField(max_length=100)
    slug          = models.SlugField(max_length=100, unique=True)
    version       = models.CharField(max_length=10, default="1.0.0")
    is_installed  = models.BooleanField(default=False)

    class Meta:
        db_table = 'modules'



class Permission(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role        = models.CharField(max_length=100, unique=True)
    is_create   = models.BooleanField(default=False)
    is_edit     = models.BooleanField(default=False)
    is_delete   = models.BooleanField(default=False)

    class Meta:
        db_table  = 'permissions'