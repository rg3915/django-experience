from django.urls import path
# from django.urls import include
from rest_framework import routers

# from backend.example.api.viewsets import ExampleViewSet
from backend.example.api.viewsets import ExampleView

app_name = 'example'

router = routers.DefaultRouter()

# router.register(r'examples', ExampleViewSet, basename='example')
# router.register(r'examples', ExampleView, basename='example')

urlpatterns = [
    # path('api/v1/', include(router.urls)),
    path('api/v1/examples/', ExampleView.as_view()),
]
