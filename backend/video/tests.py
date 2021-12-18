import json

from django.test import TestCase

from .models import Video


class VideoTest(TestCase):

    def setUp(self):
        self.payload = {
            "title": "Matrix",
            "release_year": 1999
        }

    def test_video_create(self):
        response = self.client.post(
            '/api/v1/videos/',
            data=self.payload,
            content_type='application/json'
        )
        resultado = json.loads(response.content)
        esperado = {
            "data": {
                "id": 1,
                **self.payload
            }
        }
        self.assertEqual(esperado, resultado)

    def test_video_list(self):
        Video.objects.create(**self.payload)

        response = self.client.get(
            '/api/v1/videos/',
            content_type='application/json'
        )
        resultado = json.loads(response.content)
        esperado = {
            "data": [
                {
                    "id": 1,
                    **self.payload
                }
            ]
        }
        self.assertEqual(esperado, resultado)

    def test_video_detail(self):
        Video.objects.create(**self.payload)

        response = self.client.get(
            '/api/v1/videos/1/',
            content_type='application/json'
        )
        resultado = json.loads(response.content)
        esperado = {
            "data": {
                "id": 1,
                **self.payload
            }
        }
        self.assertEqual(esperado, resultado)

    def test_video_update(self):
        Video.objects.create(**self.payload)

        data = {
            "title": "Matrix 2"
        }

        response = self.client.post(
            '/api/v1/videos/1/',
            data=data,
            content_type='application/json'
        )
        resultado = json.loads(response.content)
        esperado = {
            "data": {
                "id": 1,
                "title": "Matrix 2",
                "release_year": 1999
            }
        }
        self.assertEqual(esperado, resultado)

    def test_video_delete(self):
        Video.objects.create(**self.payload)

        response = self.client.delete(
            '/api/v1/videos/1/',
            content_type='application/json'
        )
        resultado = json.loads(response.content)
        esperado = {"data": "Item deletado com sucesso."}

        self.assertEqual(esperado, resultado)
