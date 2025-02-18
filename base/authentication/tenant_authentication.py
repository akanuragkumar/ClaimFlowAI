from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from base.middleware.custom_manager import set_current_tenant
from tenant.models import Tenants


class APIKeySecretAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('X-API-KEY')
        api_secret = request.headers.get('X-API-SECRET')

        if not api_key or not api_secret:
            raise AuthenticationFailed('API Key and Secret are required.')

        try:
            tenant = Tenants.objects.get(api_key=api_key)
        except Tenants.DoesNotExist:
            raise AuthenticationFailed('Invalid API Key.')

        if not tenant.check_api_secret(api_secret):
            raise AuthenticationFailed('Invalid API Secret.')

        set_current_tenant(tenant)
        request.tenant = tenant

        # Return the tenant as the authenticated user
        return tenant, None
