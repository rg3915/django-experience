from django.urls import include, path
from rest_framework import routers

from backend.school.api.viewsets import (
    ClassroomViewSet,
    ClassViewSet,
    GradeViewSet
)
from backend.school.api.viewsets import StudentViewSet as SimpleStudentViewSet

app_name = 'school'

router = routers.DefaultRouter()

router.register(r'students', SimpleStudentViewSet, basename='student')
router.register(r'classrooms', ClassroomViewSet, basename='classroom')
router.register(r'classes', ClassViewSet, basename='classes')
router.register(r'grades', GradeViewSet, basename='grade')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
