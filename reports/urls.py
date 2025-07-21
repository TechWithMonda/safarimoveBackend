from django.urls import path
from .views import TrafficReportCreateView, RecentTrafficUpdatesView

urlpatterns = [
    path('report/', TrafficReportCreateView.as_view(), name='create-report'),
    path('reports/recent/', RecentTrafficUpdatesView.as_view(), name='recent-reports'),
]