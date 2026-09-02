from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AdView

class AdViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdView
        fields = '__all__'