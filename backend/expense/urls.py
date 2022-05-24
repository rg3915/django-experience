from django.urls import include, path
from rest_framework import routers

app_name = 'expense'

router = routers.DefaultRouter()

# router.register(r'expenses', ExpenseViewSet, basename='expense')
# Lição de casa: completar a parte do viewsets e serializers.

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
