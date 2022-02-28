# Django Experience #09 - DRF: Entendendo Autenticação

Doc: https://www.django-rest-framework.org/api-guide/authentication/

## BasicAuthentication

É quando você faz a autenticação informando usuário e senha no cabeçalho da requisição via POST. Por exemplo, via Postman, usando `Basic Auth`.

Recomendável usar somente em testes locais.


## SessionAuthentication

É quando você faz o login pela própria interface do Django. Na tela de login do Admin, por exemplo.

O que nós chamamos de sessão é a própria autenticação default do Django.


### Configurando o login via Django (Sessão)

Edite `settings.py`

```python
LOGIN_URL = '/admin/login/'
```


Edite `urls.py`

```python
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    ...
]
```

https://docs.djangoproject.com/en/4.0/topics/auth/default/#module-django.contrib.auth.views



```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}
```

Considere a app `movie`.

```python
# movie/api/viewsets.py
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class MovieExampleView(APIView):

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
```

```python
# movie/urls.py
from backend.movie.api.viewsets import MovieExampleView

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/movie-examples/', MovieExampleView.as_view()),
]
```

Abra o Postman e faça uma requisição em `http://localhost:8000/api/v1/movie-examples/`

```python
# movie/api/viewsets.py
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

```

Abra o Postman e faça uma requisição em `http://localhost:8000/api/v1/categories/`


## TokenAuthentication

É quando você informa um token de autorização para cada usuário logado.


```python
# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken',  # <-- rode python manage.py migrate
    ...
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        ...
        'rest_framework.authentication.TokenAuthentication',
    ]
}
```

Rode `python manage.py migrate`

```python
# movie/api/viewsets.py
from rest_framework.authentication import TokenAuthentication

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
```


### Criando token

```python
from rest_framework.authtoken.models import Token

user = User.objects.get(username='admin')
token = Token.objects.create(user=user)
print(token.key)
# 74238954b49eb221559131d677a1ea84b76c735a  # (este é o meu exemplo)
```

### Autenticando via Token

#### Postman

Abra o Postman, clique em **Authorization** e escolha **No Auth**.

Depois clique em **Headers** e em **KEY** digite `Authorization` e em **VALUE** digite o seu `Token 74238954b49eb221559131d677a1ea84b76c735a` (este é o meu exemplo).

#### curl

```
curl -X GET http://localhost:8000/api/v1/examples/ -H 'Authorization: Token 74238954b49eb221559131d677a1ea84b76c735a'
curl -X GET http://localhost:8000/api/v1/categories/ -H 'Authorization: Token 74238954b49eb221559131d677a1ea84b76c735a'
```

## Djoser e JWT Authentication

Leia [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html)

Veja os videos

[Dica 47 - DRF: djoser](https://youtu.be/HUtG2Eg47Gw)

[Dica 48 - DRF: Reset de Senha com djoser](https://youtu.be/BilRdaQXX8U)

[Dica 49 - DRF: Autenticação via JWT com djoser](https://youtu.be/dOomllYxj9E)

