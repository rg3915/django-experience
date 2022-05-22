from django.urls import include, path
from rest_framework import routers

app_name = 'bookstore'

router = routers.DefaultRouter()

# router.register(r'books', BookViewSet, basename='book')
# Lição de casa: completar a parte do viewsets e serializers.

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
