from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    method = context['request'].method

    if response:
        if response.status_code == status.HTTP_403_FORBIDDEN:
            if method == 'POST':
                response.data = {'message': 'Você não tem permissão para Adicionar.'}
            elif method == 'PUT' or method == 'PATCH':
                response.data = {'message': 'Você não tem permissão para Editar.'}
            elif method == 'DELETE':
                response.data = {'message': 'Você não tem permissão para Deletar.'}

        return response
