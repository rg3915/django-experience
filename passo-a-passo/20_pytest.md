# Django Experience #20 - pytest, testando a API

<a href="">
    <img src="../img/youtube.png">
</a>

Doc: [pytest-django.readthedocs.io](https://pytest-django.readthedocs.io/en/latest/)


## Instalação

`pip install pytest-django`


`pip freeze | grep pytest-django >> requirements.txt`



Crie `pytest.ini` na pasta principal.

`touch pytest.ini`

```
[pytest]
DJANGO_SETTINGS_MODULE = backend.settings
python_files = tests.py test_*.py *_tests.py
```

Para ver se está funcionando rode no terminal

`pytest`


## Testando a app crm

Depois crie a pasta de testes dentro da app `crm`.

```bash
rm -f backend/crm/tests.py
mkdir backend/crm/tests
touch backend/crm/tests/__init__.py
touch backend/crm/tests/conftest.py
touch backend/crm/tests/test_api.py
```



Edite `conftest.py`

```python
# conftest.py
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
```

Edite `test_api.py`


```python
# test_api.py
from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_create_customer(client, customer):
    url = '/api/v1/customers/'
    response = client.post(url, customer, content_type='application/json')
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.django_db
def test_list_customers_status_code(client):
    url = '/api/v1/customers/'
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

```

Rode `pytest`. Vai dar erro.

## Corrigindo o erro.

```python
# test_api.py
from http import HTTPStatus

import pytest


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

```

## Mais testes

Vamos relembrar as regras de negócio da app `crm`.

* Crie um cadastro de **clientes**.
* Os campos são: usuário (nome, sobrenome, e-mail), vendedor (nome, sobrenome, e-mail), RG, CPF, CEP, endereço, ativo (booleano).
* Cada **cliente** pode ter um **vendedor** associado a ele, mas não é obrigatório.
* Ao **criar** um novo cliente, deve preencher os campos: usuário, RG, CPF, CEP, endereço.
* Ao **editar** um cliente, pode editar os campos: usuário (nome, sobrenome, e-mail), vendedor (nome, sobrenome, e-mail), RG, CPF, CEP, endereço.
* Retornar RG, CPF e CEP formatado com pontos e traços. Ex: 904.658.880-70
* Se eu for um Vendedor, eu só posso ver os meus clientes.
* Se eu for um Vendedor, ao cadastrar o cliente o campo "vendedor" deve ser preenchido com o usuário logado.
* Se eu for um Vendedor, só posso editar os meus clientes.

* Crie uma tabela de **comissões**.
* Os campos são: grupo e porcentagem.

* Criar um sistema de autenticação com login, logout e cadastro.

* Se eu for um Vendedor, não posso ver a tabela de comissões.
* Fazer uma validação simples de CPF e CEP para aceitar somente números.
