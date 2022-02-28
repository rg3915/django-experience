from rest_framework import serializers

from backend.example.models import Example


class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = '__all__'
