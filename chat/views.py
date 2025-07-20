from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import DisappearingMessage
from .serializers import DisappearingMessageSerializer
from django.utils import timezone
from datetime import timedelta

class ActiveMessagesView(generics.ListCreateAPIView):
    serializer_class = DisappearingMessageSerializer

    def get_queryset(self):
        cutoff = timezone.now() - timedelta(hours=24)
        return DisappearingMessage.objects.filter(sent_at__gte=cutoff)
