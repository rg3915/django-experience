# Django Experience #07 - DRF: APIView e o problema do get_extra_actions


## Criando uma app para o exemplo

Antes vamos considerar a app `example`, um model `Example` e um campo `title`.

```
python manage.py dr_scaffold example Example title:charfield
mv example backend
mkdir backend/example/api
mv backend/example/serializers.py backend/example/api
mv backend/example/views.py backend/example/api/viewsets.py
```

Edite `example/apps.py`

```python
name = 'backend.example'
```

Edite `settings.py`

```python
INSTALLED_APPS = [
    # my apps
    'backend.core',
    'backend.example',
    ...
]
```

Edite `urls.py` principal

```python
urlpatterns = [
    path('', include('backend.core.urls', namespace='core')),
    path('', include('backend.example.urls', namespace='example')),
    ...
]
```

Edite `example/admin.py`

```python
from backend.example.models import Example
```

Edite `example/urls.py`

```python
from django.urls import include, path
from rest_framework import routers

from backend.example.api.viewsets import ExampleViewSet

app_name = 'example'

router = routers.DefaultRouter()

router.register(r'examples', ExampleViewSet, basename='example')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
```

Edite `example/api/serializers.py`

```python
from backend.example.models import Example
```

Edite `example/api/viewsets.py`

```python
from backend.example.models import Example
from backend.example.api.serializers import ExampleSerializer
```

Finalmente rode

```
python manage.py makemigrations
python manage.py migrate
```


## O problema do get_extra_actions

Existem muitos tutoriais na internet, inclusive na documentação, tentando exemplificar de uma forma mais simples, o uso da [APIView](https://www.django-rest-framework.org/api-guide/views/#class-based-views).
Como no exemplo a seguir:

```python
class ExampleView(APIView):

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
```


Uma coisa que não está escrito lá, é que ao usá-lo, ele gera o seguinte erro:

```
AttributeError: 'function' object has no attribute 'get_extra_actions'
```

E mesmo que você tente implementar esse método, por exemplo:

```python
class ExampleView(APIView):
    ...

    @classmethod
    def get_extra_actions(cls):
        return []
```

De nada adianta. Na verdade o problema está no **routers**, que não reconhece esse método, mesmo que você o implemente. Ou seja, se você usar

```python
from backend.example.api.viewsets import ExampleView

router = routers.DefaultRouter()

router.register(r'examples', ExampleView, basename='example')
```

... ele não vai funcionar.

Qual é a solução?

```python
urlpatterns = [
    # path('api/v1/', include(router.urls)),
    path('api/v1/examples/', ExampleView.as_view()),
]
```

E não precisa implementar o `get_extra_actions`.

Resolvido o problema. :)

