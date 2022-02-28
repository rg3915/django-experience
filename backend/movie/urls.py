from django.urls import include, path
from rest_framework import routers

from backend.movie.api.viewsets import (
    CategoryViewSet,
    MovieExampleView,
    MovieViewSet
)

app_name = 'movie'

router = routers.DefaultRouter()

router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/movie-examples/', MovieExampleView.as_view()),
]
