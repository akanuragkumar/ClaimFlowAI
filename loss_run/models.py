from django.db import models
from base.middleware.custom_manager import TenantAwareManager
from base.models import BaseModel
from tenant.models import Tenants
from datetime import datetime

class LossRunReport(BaseModel):
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE)  # Tenant identifier
    is_processed = models.BooleanField(default=False)
    raw_file = models.FileField(upload_to="loss_runs_pdf/")  # Store uploaded file
    report_image = models.ImageField(upload_to="loss_run_reports/", null=True, blank=True)  # Stores generated report

    # Use the tenant-aware manager
    objects = TenantAwareManager()

    def __str__(self):
        return f"LossRunReport {self.id} - Processed: {self.is_processed}"

    class Meta:
        app_label = 'loss_run'
        verbose_name = "Loss_run_report"
        verbose_name_plural = "Loss_run_reports"


class LossRunRecord(models.Model):
    loss_run_report = models.ForeignKey(LossRunReport, on_delete=models.CASCADE, related_name="records")
    policy_number = models.CharField(max_length=50)
    policy_period_start = models.DateField(null=True, blank=True)
    policy_period_end = models.DateField(null=True, blank=True)
    loss_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    total_incurred = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    claim_sentiment = models.CharField(max_length=50, null=True, blank=True)
    claim_summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.policy_number} - {self.status}"

    class Meta:
        app_label = 'loss_run'
        verbose_name = "Loss_run_record"
        verbose_name_plural = "Loss_run_records"
