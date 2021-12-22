# Django Experience #07 - DRF: APIView e o problema do get_extra_actions

Existem muitos tutoriais na internet, inclusive na documentação, tentando exemplificar de uma forma mais simples, o uso da [APIView](https://www.django-rest-framework.org/api-guide/views/#function-based-views).
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

```
router = routers.DefaultRouter()

router.register(r'examples', ExampleView, basename='example')
```

... ele não vai funcionar.

Qual é a solução?

```python
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/examples/', ExampleView.as_view()),
]
```

E não precisa implementar o `get_extra_actions`.

Resolvido o problema. :)


