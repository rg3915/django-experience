from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.example.api.serializers import ExampleSerializer
from backend.example.models import Example


class ExampleViewSet(viewsets.ModelViewSet):
    queryset = Example.objects.all()
    serializer_class = ExampleSerializer


class ExampleView(APIView):

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth)
        }
        return Response(content)

    # Não serve
    # @classmethod
    # def get_extra_actions(cls):
    #     return []
