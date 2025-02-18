from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from base.authentication.tenant_authentication import APIKeySecretAuthentication
from base.middleware.CustomMetaDataMixin import CustomMetaDataMixin
from loss_run.serializers import LossRunReportSerializer, LossRunRecordSerializer
from loss_run.handlers.upload_report import process_loss_run_file

class LossRunUploadView(CustomMetaDataMixin, APIView):
    authentication_classes = [APIKeySecretAuthentication]
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded"}, status=HTTP_400_BAD_REQUEST)

        try:
            loss_run_report, saved_records = process_loss_run_file(request.tenant, file)
            return Response(
                {
                    "message": "Data extracted successfully, processing started",
                    "report": LossRunReportSerializer(loss_run_report).data,
                    "records": LossRunRecordSerializer(saved_records, many=True).data,
                },
                status=HTTP_201_CREATED
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
