from http import HTTPStatus
from rest_framework import serializers

import pytest

from backend.movie.models import Movie
from backend.movie.api.serializers import MovieSerializer


@pytest.mark.django_db
def test_create_movie(client, seller):
    url = '/api/v1/movies/'

    client.force_login(seller)

    data = {
        "title": "string",
        "sinopse": "string",
        "rating": 3,
        "censure": 1,
        "like": True,
        "category": {
            "title": "string"
        }
    }

    response = client.post(url, data, content_type='application/json')

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.django_db
def test_create_movie_error(client, seller):
    url = '/api/v1/movies/'

    client.force_login(seller)

    data = {
        "title": "lorem",
        "sinopse": "string",
        "rating": 3,
        "censure": 1,
        "like": True,
        "category": {
            "title": "string"
        }
    }

    response = client.post(url, data, content_type='application/json')
    # assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['non_field_errors'][0] == 'Lorem não pode.'


def test_serializer_falha_titulo():
    data = {
        "title": "lorem",
        "sinopse": "string",
        "rating": 3,
        "censure": 1,
        "like": True,
        "category": {
            "title": "string"
        }
    }
    serializer = MovieSerializer(data=data)
    serializer.is_valid()

    error = serializer.errors["non_field_errors"]
    assert "Lorem não pode" in str(error[0])
