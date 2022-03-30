from django.urls import include, path
from rest_framework import routers

from backend.crm.api.viewsets import ComissionViewSet, CustomerViewSet

app_name = 'crm'

router = routers.DefaultRouter()

router.register(r'comissions', ComissionViewSet, basename='comission')
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
