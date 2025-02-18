from collections import OrderedDict
from django.http.response import HttpResponseBase
from rest_framework import status
from rest_framework.response import Response


class CustomMetaDataMixin(object):
    """
    When you Inherit from this Mixin, remember to keep it to the left of any ApiView subclass,
    else this mixin's finalize_response() method won't override ApiView's
    """

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Returns the final response object.
        """
        # Make the error obvious if a proper response is not returned
        assert isinstance(response, HttpResponseBase), (
            'Expected a `Response`, `HttpResponse` or `HttpStreamingResponse` '
            'to be returned from the view, but received a `%s`'
            % type(response)
        )
        if isinstance(response, Response):
            if not getattr(request, 'accepted_renderer', None):
                neg = self.perform_content_negotiation(request, force=True)
                request.accepted_renderer, request.accepted_media_type = neg

            response.accepted_renderer = request.accepted_renderer
            response.accepted_media_type = request.accepted_media_type
            response.renderer_context = self.get_renderer_context()

        for key, value in self.headers.items():
            response[key] = value

        response = self.envelope_response(request, response)

        # Override Status for bubble integration
        if response.has_header("OverrideStatus200"):
            response.status_code = status.HTTP_200_OK

        return response

    def envelope_response(self, request, response):
        if response.data and 'meta' in response.data:
            response.data['meta'].update(self.get_response_meta(request, response))
            response_meta = response.data['meta']
            response_data = response.data['data']
        else:
            response_meta = self.get_response_meta(request, response)
            if response_meta.get("is_error"):
                response_data = []
            else:
                response_data = response.data

        if response.exception:
            response_data = []

        envelope = OrderedDict([('meta', response_meta), ('data', response_data)])
        response.data = envelope
        return response

    @staticmethod
    def get_response_meta(request, response):
        msg = "Success"
        _error = None
        _is_error = False
        if response.exception or response.status_code not in (status.HTTP_200_OK, status.HTTP_201_CREATED,
                                                              status.HTTP_204_NO_CONTENT):
            msg = "Something went wrong."
            _error = response.data
            _is_error = True

        response_meta = {
            "status": response.status_code,
            "is_error": _is_error,
            "message": msg,
            "error": _error
        }
        return response_meta
