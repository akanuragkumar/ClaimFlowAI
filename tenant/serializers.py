# tenant/serializers.py
from rest_framework import serializers
from tenant.models import Tenants

class TenantCreateSerializer(serializers.ModelSerializer):
    api_secret = serializers.CharField(write_only=True)

    class Meta:
        model = Tenants
        fields = ['name', 'address', 'phone_number', 'email', 'api_secret']

class TenantResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenants
        fields = ['uuid', 'name', 'address', 'phone_number', 'email', 'api_key', 'created', 'modified']

class TenantUpdateSerializer(serializers.ModelSerializer):
    api_secret = serializers.CharField(required=False, write_only=True)
    regenerate_api_key = serializers.BooleanField(required=False)

    class Meta:
        model = Tenants
        fields = ['api_secret', 'regenerate_api_key']
