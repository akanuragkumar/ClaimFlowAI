import threading

from django.db import models


class TenantAwareManager(models.Manager):
    """Automatically filters queries by the current tenant"""

    def get_queryset(self):
        # Access the current tenant from the global request (in middleware)

        current_tenant = get_current_tenant()  # This function will return the tenant set in middleware
        if current_tenant:
            return super().get_queryset().filter(tenant=current_tenant)
        return super().get_queryset()

    def create(self, **kwargs):
        # Automatically assign tenant if not provided
        current_tenant = get_current_tenant()
        if current_tenant and 'tenant' not in kwargs:
            kwargs['tenant'] = current_tenant
        return super().create(**kwargs)


# Thread-local storage to hold the current tenant (tenant)
_thread_locals = threading.local()


def get_current_tenant():
    """Return the current tenant (tenant) stored in thread-local storage"""
    return getattr(_thread_locals, 'tenant', None)


def set_current_tenant(tenant):
    """Set the current tenant (tenant) in thread-local storage"""
    _thread_locals.tenant = tenant
