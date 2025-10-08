from django.urls import include, path
from rest_framework import routers

from backend.hotel.api.viewsets import HotelViewSet

app_name = 'hotel'

router = routers.DefaultRouter()

router.register(r'hotels', HotelViewSet, basename='hotel')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]

# api/v1/hotels/            GET, POST
# api/v1/hotels/<int:pk>/   GET, PATCH, PUT, DELETE
