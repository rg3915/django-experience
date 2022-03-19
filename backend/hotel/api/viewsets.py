from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from backend.hotel.api.serializers import HotelSerializer
from backend.hotel.models import Hotel


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = (AllowAny,)
