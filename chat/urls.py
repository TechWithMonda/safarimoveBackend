from django.urls import path
from .views import ActiveMessagesView

urlpatterns = [
    path('messages/', ActiveMessagesView.as_view(), name='messages'),
]
