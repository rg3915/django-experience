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
