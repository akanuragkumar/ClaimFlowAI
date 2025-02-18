from django.db import models
import bcrypt
import uuid

from base.models import BaseModel


class Tenants(BaseModel):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    # API Authentication Fields
    api_key = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    api_secret_hash = models.CharField(max_length=128)  # Hashed secret

    def set_api_secret(self, api_secret):
        """Hashes the API secret and stores the hash in the database"""
        salt = bcrypt.gensalt()
        self.api_secret_hash = bcrypt.hashpw(api_secret.encode('utf-8'), salt).decode('utf-8')

    def check_api_secret(self, api_secret):
        """Verifies the provided API secret against the stored hash"""
        return bcrypt.checkpw(api_secret.encode('utf-8'), self.api_secret_hash.encode('utf-8'))

    def regenerate_api_credentials(self):
        """Generates a new API key and secret for the tenant"""
        new_api_key = str(uuid.uuid4())
        new_api_secret = uuid.uuid4().hex
        self.api_key = new_api_key
        self.set_api_secret(new_api_secret)
        return new_api_key, new_api_secret

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'tenant'
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'
