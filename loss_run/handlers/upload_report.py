from django.core.files.storage import default_storage
from loss_run.models import LossRunReport
from loss_run.serializers import LossRunRecordSerializer
from loss_run.tasks import (
    enrich_loss_run_data,
    generate_loss_run_report,
    sentiment_analysis_for_claims
)
from loss_run.utils import extract_loss_run_data

def process_loss_run_file(tenant, file):
    """
    Process the uploaded loss run file, extract data, save records, and trigger background tasks.
    """
    try:
        # Create LossRunReport instance
        loss_run_report = LossRunReport.objects.create(
            tenant=tenant,
            raw_file=file
        )

        # Extract data from the PDF
        extracted_data = extract_loss_run_data(default_storage.path(loss_run_report.raw_file.path))

        if not extracted_data:
            raise ValueError("No valid loss run data found in the uploaded report")

        # Flatten the list of lists
        extracted_data = [item for sublist in extracted_data for item in sublist]

        saved_records = []
        for item in extracted_data:
            # Include the loss_run_report in the data
            item['loss_run_report'] = loss_run_report.id
            serializer = LossRunRecordSerializer(data=item)
            if serializer.is_valid():
                record = serializer.save()
                saved_records.append(record)
            else:
                raise ValueError(serializer.errors)

        # Mark the report as processed
        loss_run_report.is_processed = True
        loss_run_report.save()

        # Trigger background tasks
        enrich_loss_run_data.delay(loss_run_report.id)
        sentiment_analysis_for_claims.delay(loss_run_report.id)
        generate_loss_run_report.delay(loss_run_report.id)

        return loss_run_report, saved_records

    except Exception as e:
        # Handle exceptions and clean up if necessary
        print(f"Error processing loss run file: {e}")
        raise
