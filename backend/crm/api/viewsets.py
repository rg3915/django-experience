from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import BasePermission

from backend.crm.api.serializers import (
    ComissionSerializer,
    CustomerCreateSerializer,
    CustomerSerializer,
    CustomerUpdateSerializer
)
from backend.crm.models import Comission, Customer


class CustomerViewSet(viewsets.ModelViewSet):
    # queryset = Customer.objects.all()
    # serializer_class = CustomerSerializer
    filter_backends = (SearchFilter,)
    search_fields = (
        'user__first_name',
        'user__last_name',
        'user__email',
        'seller__first_name',
        'seller__last_name',
        'seller__email',
        'rg',
        'cpf',
        'cep',
        'address',
    )

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomerCreateSerializer

        if self.action == 'update' or self.action == 'partial_update':
            return CustomerUpdateSerializer

        return CustomerSerializer

    def is_seller(self, seller):
        if seller:
            groups_list = seller.groups.values_list('name', flat=True)
            return True if 'Vendedor' in groups_list else False
        return False

    def get_queryset(self):
        '''
        Vendedor só pode ver os seus clientes.
        '''
        seller = self.request.user
        queryset = Customer.objects.all()

        active = self.request.query_params.get('active')

        if active is not None:
            queryset = queryset.filter(active=active)

        if self.is_seller(seller):
            queryset = queryset.filter(seller=seller)
            return queryset

        return queryset

    def perform_create(self, serializer):
        '''
        Ao criar um objeto, se for Vendedor, então define seller com o usuário logado.
        '''
        seller = self.request.user

        if self.is_seller(seller):
            serializer.save(seller=seller)
        else:
            serializer.save()

    def perform_update(self, serializer):
        '''
        O Vendedor só pode editar os clientes dele.
        '''
        instance = self.get_object()

        if self.is_seller(instance.seller) and self.request.user == instance.seller:
            serializer.save()
        else:
            raise DRFValidationError('Você não tem permissão para editar este registro.')


class NotSellerPermission(BasePermission):
    message = 'Você não tem permissão para visualizar este registro.'

    def is_seller(self, seller):
        if seller:
            groups_list = seller.groups.values_list('name', flat=True)
            return True if 'Vendedor' in groups_list else False
        return False

    def has_permission(self, request, view):
        seller = request.user

        if self.is_seller(seller):
            response = {
                'message': self.message,
                'status_code': status.HTTP_403_FORBIDDEN
            }
            raise DRFValidationError(response)
        else:
            return True


class ComissionViewSet(viewsets.ModelViewSet):
    queryset = Comission.objects.all()
    serializer_class = ComissionSerializer
    permission_classes = (NotSellerPermission,)
