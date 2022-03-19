from rest_framework import serializers

from backend.hotel.models import Hotel


class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = '__all__'

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('A data inicial deve ser anterior ou igual a data final!')
        return data
