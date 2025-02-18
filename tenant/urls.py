from django.urls import path

from tenant.views import TenantView

urlpatterns = [
    # Onboard a new tenant (POST)
    path('', TenantView.as_view(), name='tenant_onboard'),

    # Get tenant details and update (GET, PUT)
    path('<uuid:tenant_uuid>/', TenantView.as_view(), name='tenant_details'),
]
