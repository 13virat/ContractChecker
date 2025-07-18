from rest_framework import serializers
from .models import Comparison

class ComparisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comparison
        fields = '__all__'