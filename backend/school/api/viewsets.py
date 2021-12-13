from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from backend.school.api.serializers import (
    ClassAddSerializer,
    ClassroomSerializer,
    ClassSerializer,
    GradeSerializer,
    StudentRegistrationSerializer,
    StudentSerializer,
    StudentUpdateSerializer
)
from backend.school.models import Class, Classroom, Grade, Student

# class StudentViewSet(viewsets.ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer


class StudentViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving students.
    Uma ViewSet simples para listar ou recuperar alunos.
    """

    def get_serializer_class(self):
        # Muda o serializer dependendo da ação.
        if self.action == 'create':
            return StudentSerializer

        if self.action == 'update':
            return StudentUpdateSerializer

        return StudentSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        queryset = Student.objects.all()
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(queryset, pk=pk)
        return obj

    def list(self, request):
        # queryset = Student.objects.all()
        # serializer = StudentSerializer(queryset, many=True)
        # return Response(serializer.data)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        # Sem paginação
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        queryset = Student.objects.all()
        student = get_object_or_404(queryset, pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, pk=None):
        item = self.get_object()
        item.delete
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def all_students(self, request, pk=None):
        queryset = Student.objects.all()
        serializer = StudentRegistrationSerializer(queryset, many=True)
        return Response(serializer.data)


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = (AllowAny,)


class GradeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = (AllowAny,)


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    # serializer_class = ClassSerializer

    # def list(self, request, *args, **kwargs):
    #     user = self.request.user
    #     teacher = User.objects.get(username=user)

    #     if user is not None:
    #         queryset = Class.objects.filter(teacher=teacher)
    #     else:
    #         queryset = Class.objects.none()

    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    def get_queryset(self):
        '''
        Retorna somente as aulas da pessoa logada no momento.
        '''
        user = self.request.user
        teacher = User.objects.get(username=user)

        if user is not None:
            queryset = Class.objects.filter(teacher=teacher)
        else:
            queryset = Class.objects.none()

        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return ClassAddSerializer

        if self.action == 'update':
            return ClassSerializer

        return ClassSerializer

    def perform_create(self, serializer):
        '''
        Ao criar um objeto, define teacher com o usuário logado.
        '''
        user = self.request.user
        teacher = User.objects.get(username=user)

        if user is not None:
            serializer.save(teacher=teacher)

    def create(self, request, *args, **kwargs):
        # https://www.cdrf.co/3.12/rest_framework.viewsets/ModelViewSet.html#create
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        user = self.request.user
        data = self.request.data
        teacher_id = data.get('teacher')

        try:
            teacher = User.objects.get(pk=teacher_id)
        except User.DoesNotExist:
            raise DRFValidationError('Usuário não encontrado.')

        if user and user.is_authenticated:
            if user == teacher:
                serializer.save()
            else:
                raise DRFValidationError('Você não tem permissão para esta operação.')

    def retrieve(self, request, *args, **kwargs):
        '''
        Método para ver os detalhes.
        '''
        instance = self.get_object()
        teacher = instance.teacher
        user = self.request.user

        if user and user.is_authenticated:
            if user == teacher:
                serializer = self.get_serializer(instance)
            else:
                raise DRFValidationError('Você não tem acesso a esta aula.')

        return Response(serializer.data)

    def perform_destroy(self, instance):
        '''
        Método pra deletar os dados.
        '''
        # instance.delete()
        raise DRFValidationError('Nenhuma aula pode ser deletada.')
