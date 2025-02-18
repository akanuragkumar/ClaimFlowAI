import uuid
from django.db import models

class BaseModel(models.Model):
    """This is a common model which is to be inherited on all other models."""
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
