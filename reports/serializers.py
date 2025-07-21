from rest_framework import serializers
from .models import TrafficReport

class TrafficReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficReport
        fields = ['id', 'location', 'message', 'severity', 'created_at']
        read_only_fields = ['id', 'created_at']