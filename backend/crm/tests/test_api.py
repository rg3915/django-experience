from http import HTTPStatus

import pytest

from backend.crm.models import Customer
from backend.crm.api.serializers import (
    CustomerCreateSerializer,
    CustomerUpdateSerializer,
    CustomerSerializer
)


@pytest.mark.django_db
def test_create_customer(client, customer, seller):
    url = '/api/v1/customers/'

    # https://pytest-django.readthedocs.io/en/latest/helpers.html?highlight=auth#id2
    client.force_login(seller)

    response = client.post(url, customer, content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.django_db
def test_list_customers_status_code(client, seller):
    url = '/api/v1/customers/'

    client.force_login(seller)

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK


def test_customer_create_contains_expected_fields():
    data = CustomerCreateSerializer().data
    expected = set(['user', 'rg', 'cpf', 'cep', 'address'])

    assert set(data.keys()) == expected


def test_customer_update_contains_expected_fields():
    data = CustomerUpdateSerializer().data
    expected = set(['user', 'seller', 'rg', 'cpf', 'cep', 'address'])

    assert set(data.keys()) == expected


@pytest.mark.django_db
def test_customer_representation(user):
    '''
    Retornar RG, CPF e CEP formatado com pontos e traços. Ex: 904.658.880-70
    '''
    data = {
        "user": user,
        "rg": "207629010",
        "cpf": "35703019079",
        "cep": "04013000",
        "address": "Rua Cubatão, 220 - São Paulo - SP"
    }
    customer = Customer.objects.create(**data)

    rg = f"{customer.rg[:2]}.{customer.rg[2:5]}.{customer.rg[5:8]}-{customer.rg[8:]}"
    cpf = f"{customer.cpf[:3]}.{customer.cpf[3:6]}.{customer.cpf[6:9]}-{customer.cpf[9:]}"
    cep = f"{customer.cep[:5]}-{customer.cep[5:]}"

    assert rg == '20.762.901-0'
    assert cpf == '357.030.190-79'
    assert cep == '04013-000'
