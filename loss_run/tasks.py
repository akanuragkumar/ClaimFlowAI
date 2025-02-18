import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from io import BytesIO

from openai import OpenAI

from loss_run.models import LossRunRecord, LossRunReport

client = OpenAI(api_key=settings.OPENAI_API_KEY)


@shared_task
def enrich_loss_run_data(loss_run_report_id):
    """Use OpenAI API to generate claim summaries and sentiment analysis."""
    try:
        loss_run_records = LossRunRecord.objects.filter(loss_run_report_id=loss_run_report_id)

        for record in loss_run_records:
            description = f"Summarize this claim in one sentence: {record.description}, occurred on {record.loss_date}, reported on {record.loss_date}."

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Summarize the following claim in one sentence:"},
                    {"role": "user", "content": description},
                ],
            )

            record.claim_summary = response.choices[0].message.content
            record.save()

        return f"Generated claim summaries for {loss_run_records.count()} records."

    except Exception as e:
        return f"Error during claim summarization: {str(e)}"


@shared_task
def generate_loss_run_report(loss_run_report_id):
    """Generate a claims report visualization and save it to the database."""
    try:
        loss_run_records = LossRunRecord.objects.filter(loss_run_report_id=loss_run_report_id)

        periods = [str(record.policy_period_start) for record in loss_run_records]
        claims_status = [1 if record.status == 'Closed' else 0 for record in loss_run_records]

        plt.figure(figsize=(10, 5))
        plt.plot(periods, claims_status, marker="o")
        plt.title("Claims Status Over Policy Periods")
        plt.xlabel("Policy Period")
        plt.ylabel("Claims Status")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save plot to memory
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)

        # Store image in the database
        loss_run_report = LossRunReport.objects.get(id=loss_run_report_id)
        loss_run_report.report_image.save(f"report_{loss_run_report_id}.png", ContentFile(buffer.getvalue()))
        buffer.close()

        return f"Report generated for LossRunReport {loss_run_report_id}."

    except Exception as e:
        return f"Error generating report: {str(e)}"


@shared_task
def sentiment_analysis_for_claims(loss_run_report_id):
    """Analyze sentiment of claim descriptions to understand urgency or severity."""
    try:
        loss_run_records = LossRunRecord.objects.filter(loss_run_report_id=loss_run_report_id)

        for record in loss_run_records:
            description = f"Analyze the sentiment of this claim: {record.claim_summary}"

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Analyze the sentiment of the following claim summary:"},
                    {"role": "user", "content": description},
                ],
            )

            record.claim_sentiment = response.choices[0].message.content
            record.save()

        return f"Sentiment analysis completed for {loss_run_records.count()} records."

    except Exception as e:
        return f"Error during sentiment analysis: {str(e)}"
