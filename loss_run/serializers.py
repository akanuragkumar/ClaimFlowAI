from rest_framework import serializers
from loss_run.models import LossRunReport, LossRunRecord

class LossRunReportResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LossRunReport
        fields = "__all__"

class LossRunRecordResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LossRunRecord
        fields = "__all__"

class LossRunRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LossRunRecord
        fields = '__all__'

    def validate_policy_number(self, value):
        if not value:
            raise serializers.ValidationError("Policy number is required.")
        return value

    def validate_status(self, value):
        if value not in ['Closed', 'Open']:
            raise serializers.ValidationError("Status must be either 'Closed' or 'Open'.")
        return value

    def validate_total_incurred(self, value):
        if value < 0:
            raise serializers.ValidationError("Total incurred must be a non-negative number.")
        return value

class LossRunReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LossRunReport
        fields = '__all__'

    def validate(self, data):
        if 'raw_file' not in data:
            raise serializers.ValidationError("A raw file is required.")
        return data
