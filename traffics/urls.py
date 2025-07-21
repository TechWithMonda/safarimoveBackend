from django.urls import path
from .views import get_traffic_data

urlpatterns = [
    path('traffic/', get_traffic_data, name='traffic-data'),
]
