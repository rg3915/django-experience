from rest_framework import status, viewsets
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication
)
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.permissions import (
    BasePermission,
    DjangoModelPermissions,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.movie.api.serializers import (
    CategorySerializer,
    MovieReadOnlySerializer,
    MovieSerializer
)
from backend.movie.models import Category, Movie


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # authentication_classes = (
    #     BasicAuthentication,
    #     SessionAuthentication,
    #     TokenAuthentication
    # )
    # permission_classes = (IsAuthenticated,)


class CensurePermission(BasePermission):
    age_user = 14
    group_name = 'Infantil'
    message = 'Este filme não é permitido para este perfil.'

    # def has_permission(self, request, view):
    #     # Retorna uma lista de todos os grupos do usuário logado.
    #     groups = request.user.groups.values_list('name', flat=True)

    #     try:
    #         # Pega a instância do objeto.
    #         obj = view.get_object()
    #     except AssertionError:
    #         return True

    #     censure = obj.censure

    #     if self.group_name in groups and censure >= self.age_user:
    #         response = {
    #             'message': self.message,
    #             'status_code': status.HTTP_403_FORBIDDEN
    #         }
    #         raise DRFValidationError(response)
    #     else:
    #         return True

    def has_object_permission(self, request, view, obj):
        # Retorna uma lista de todos os grupos do usuário logado.
        groups = request.user.groups.values_list('name', flat=True)

        censure = obj.censure

        if self.group_name in groups and censure >= self.age_user:
            response = {
                'message': self.message,
                'status_code': status.HTTP_403_FORBIDDEN
            }
            raise DRFValidationError(response)
        else:
            return True


class NotDeletePermission(BasePermission):
    message = 'Nenhum registro pode ser deletado.'

    def has_permission(self, request, view):
        if request.method == 'DELETE':
            response = {
                'message': self.message,
                'status_code': status.HTTP_403_FORBIDDEN
            }
            raise DRFValidationError(response)
        else:
            return True


class MovieViewSet(viewsets.ModelViewSet):
    # queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    permission_classes = (DjangoModelPermissions, CensurePermission, NotDeletePermission)

    def get_queryset(self):
        return Movie.objects.all()

    @action(detail=False, methods=['get'])
    def get_good_movies(self, request, pk=None):
        '''
        Retorna somente filmes bons, com rating maior ou igual a 4.
        '''
        movies = Movie.objects.filter(rating__gte=4)

        page = self.paginate_queryset(movies)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def movies_readonly(self, request, pk=None):
        movies = Movie.objects.all()

        page = self.paginate_queryset(movies)
        if page is not None:
            serializer = MovieReadOnlySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = MovieReadOnlySerializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def movies_regular_readonly(self, request, pk=None):
        movies = Movie.objects.all()

        page = self.paginate_queryset(movies)
        if page is not None:
            serializer = [movie.to_dict() for movie in page]
            return self.get_paginated_response(serializer)

        serializer = [movie.to_dict() for movie in movies]
        return Response(serializer)


class MovieExampleView(APIView):

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
