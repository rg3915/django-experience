from django.urls import include, path
from rest_framework import routers

from backend.school.api.viewsets import ClassroomViewSet, StudentViewSet

app_name = 'school'

router = routers.DefaultRouter()

router.register(r'students', StudentViewSet)
router.register(r'classrooms', ClassroomViewSet)

urlpatterns = [
    path("api/v1/school/", include(router.urls)),
]
