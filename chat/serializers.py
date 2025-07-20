from rest_framework import serializers
from .models import DisappearingMessage

class DisappearingMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisappearingMessage
        fields = '__all__'
