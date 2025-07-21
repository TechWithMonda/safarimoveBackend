from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import TrafficReport
from .serializers import TrafficReportSerializer
from django.utils import timezone
from datetime import timedelta

class TrafficReportCreateView(generics.CreateAPIView):
    queryset = TrafficReport.objects.all()
    serializer_class = TrafficReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Return the created report data including the auto-generated fields
        headers = self.get_success_headers(serializer.data)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)

class RecentTrafficUpdatesView(generics.ListAPIView):
    serializer_class = TrafficReportSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        # Get reports from last 24 hours
        time_threshold = timezone.now() - timedelta(hours=24)
        return TrafficReport.objects.filter(
            created_at__gte=time_threshold
        ).order_by('-created_at')[:20]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        })