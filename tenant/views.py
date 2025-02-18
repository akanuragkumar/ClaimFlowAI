# tenant/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK

from base.middleware.CustomMetaDataMixin import CustomMetaDataMixin
from tenant.serializers import TenantCreateSerializer, TenantResponseSerializer, TenantUpdateSerializer
from tenant.models import Tenants
from base.authentication.tenant_authentication import APIKeySecretAuthentication


class TenantView(CustomMetaDataMixin, APIView):
    def get_authenticators(self):
        if self.request.method in ['GET', 'PUT']:
            return [APIKeySecretAuthentication()]
        return []

    # POST: Onboard a new tenant (No authentication required)
    def post(self, request):
        serializer = TenantCreateSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            api_secret = data.pop('api_secret')

            tenant = Tenants(**data)
            tenant.set_api_secret(api_secret)
            tenant.save()

            response_serializer = TenantResponseSerializer(tenant)
            return Response(response_serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # GET: Retrieve tenant details (Authenticated)
    def get(self, request, *args, **kwargs):
        tenant = request.user  # Tenant comes from authentication
        serializer = TenantResponseSerializer(tenant)
        return Response(serializer.data, status=HTTP_200_OK)

    # PUT: Change API secret or regenerate API key (Authenticated)
    def put(self, request, *args, **kwargs):
        tenant = request.user  # Tenant comes from authentication
        serializer = TenantUpdateSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            if 'api_secret' in data:
                api_secret = data['api_secret']
                tenant.set_api_secret(api_secret)
                tenant.save()
                return Response({'status': 'API secret updated successfully.'}, status=HTTP_200_OK)

            if data.get('regenerate_api_key'):
                new_api_key, new_api_secret = tenant.regenerate_api_credentials()
                tenant.save()
                return Response({
                    'status': 'API key and secret regenerated successfully.',
                    'new_api_key': new_api_key,
                    'new_api_secret': new_api_secret
                }, status=HTTP_200_OK)

            return Response({'error': 'Invalid request. Please provide either api_secret or regenerate_api_key.'},
                            status=HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
