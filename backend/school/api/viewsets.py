from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.school.api.serializers import (
    ClassroomSerializer,
    StudentRegistrationSerializer,
    StudentSerializer
)
from backend.school.models import Classroom, Student


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=False, methods=['get'])
    def all_students(self, request, pk=None):
        queryset = Student.objects.all()
        serializer = StudentRegistrationSerializer(queryset, many=True)
        return Response(serializer.data)


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
