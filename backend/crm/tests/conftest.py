import pytest
from django.contrib.auth.models import User


@pytest.fixture
def user():
    data = {
        "username": "huguinho",
        "first_name": "Huguinho",
        "last_name": "Donald",
        "email": "huguinho@email.com"
    }
    user = User.objects.create(**data)
    return user


@pytest.fixture
def seller():
    data = {
        "username": "jordan",
        "first_name": "Jordan",
        "last_name": "Belfort",
        "email": "belfort@email.com"
    }
    user = User.objects.create(**data)
    return user


@pytest.fixture
def customer(user, seller):
    data = {
        "user": user.pk,
        "seller": seller.pk,
        "rg": "207629010",
        "cpf": "35703019079",
        "cep": "04013000",
        "address": "Rua Cubatão, 220 - São Paulo - SP"
    }
    return data
