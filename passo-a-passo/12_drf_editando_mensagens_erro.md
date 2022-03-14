# Django Experience #12 - Dica: Editando as mensagens de erro


```python
# core/handler.py
from rest_framework.views import exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    method = context['request'].method

    if response.status_code == status.HTTP_403_FORBIDDEN:
        if method == 'POST':
            response.data = {'message': 'Você não tem permissão para Adicionar.'}
        elif method == 'PUT' or method == 'PATCH':
            response.data = {'message': 'Você não tem permissão para Editar.'}
        elif method == 'DELETE':
            response.data = {'message': 'Você não tem permissão para Deletar.'}

    return response
```

```python
# settings.py
REST_FRAMEWORK = {
    ...
    'EXCEPTION_HANDLER': 'backend.core.handler.custom_exception_handler',
    ...
}
```
