# Django Experience #11 - DRF: Entendendo Permissões


Doc: https://www.django-rest-framework.org/api-guide/permissions/


## IsAuthenticated

Se você define em `settings.py`

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
```

você não precisa declarar em todas as Viewsets, por isso fica global.

Se você não definir o padrão é:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
```

Onde o acesso é liberado para tudo, mas você não precisa definir isso, pois é o default do Django.


## IsAuthenticatedOrReadOnly

Se você não estiver autenticado, você só poderá **ler**, acessar o `GET`. Caso esteja autenticado, então os outros métodos serão liberados. Exemplo, você pode **ver** os `movies`, mas não pode editar.

**Exemplo**


```python
# movie/api/viewsets.py
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class MovieViewSet(viewsets.ModelViewSet):
    ...
    permission_classes = (IsAuthenticatedOrReadOnly,)
```

Entre no Postman, e faça um **GET** sem autenticação em http://localhost:8000/api/v1/movies/

Depois faça um **POST** sem autenticação em http://localhost:8000/api/v1/movies/


```
{
  "title": "Inception",
  "rating": 5,
  "like": true
}
```

Depois tente com autenticação.


## Permissões a nível de objeto (Object level permissions)

É chamado, por exemplo, quando é executada uma instância do model.

As permissões rodam quando `.get_object()` é chamado.




## Referência da API (API Reference)

### AllowAny

Acesso liberado para todos.


### IsAuthenticated

Exige que o usuário esteja autenticado.


### IsAdminUser

Somente usuários do tipo `user.is_staff` igual a `True` podem acessar.


### IsAuthenticatedOrReadOnly

Qualquer um pode acessar o método `GET`, os demais métodos exige autenticação.


### DjangoModelPermissions

São as permissões em nível de model, definidas pelo Django Admin.

| Método | Permissão   |
|--------|-------------|
| GET    | view        |
| POST   | add         |
| PUT    | change      |
| DELETE | delete      |

**Exemplo**

Vamos criar um **grupo** chamado *Editor*. Significa que o usuário que for *Editor* poderá **editar** o filme, caso contrário só podem **ler**.

* **Importante:** O usuário **não** pode ser *super usuário*, então deve ser `user.is_superuser = False`.
* Crie o grupo *Editor*.
* Adicione a permissão `movie | Can change movie` a este grupo.
* Associe este grupo ao seu usuário.

```python
# movie/api/viewsets.py
class MovieViewSet(viewsets.ModelViewSet):
    ...
    permission_classes = (DjangoModelPermissions,)
```

Tente fazer o `PUT` com um usuário fora do grupo.

Depois tente com um usuário do grupo.


**Exemplo**

Vamos criar um **grupo** chamado *Criador*. Ele poderá **criar** ou **editar**.

* Crie o grupo *Criador*.
* Adicione a permissão `movie | Can add movie` a este grupo.
* Adicione a permissão `movie | Can change movie` a este grupo.
* Associe este grupo ao seu usuário.

Tente fazer o `POST` com um usuário fora do grupo.

Depois tente com um usuário do grupo.

Depois faça o mesmo com `PUT`.


### Custom permissions

Vamos considerar que se um usuário for do perfil *Infantil* e a censura do filme for 14 anos, então ele não poderá ver os detalhes do filme.

```python
#movie/viewsets.py
class CensurePermission(BasePermission):
    age_user = 14
    group_name = 'Infantil'
    message = 'Este filme não é permitido para este perfil.'

    def has_permission(self, request, view):
        # Retorna uma lista de todos os grupos do usuário logado.
        groups = request.user.groups.values_list('name', flat=True)

        # Pega a instância do objeto.
        obj = view.get_object()

        censure = obj.censure

        if self.group_name in groups and censure >= self.age_user:
            response = {
                'message': self.message,
                'status_code': status.HTTP_403_FORBIDDEN
            }
            raise DRFValidationError(response)
        else:
            return True


class MovieViewSet(viewsets.ModelViewSet):
    ...
    permission_classes = (DjangoModelPermissions, CensurePermission)
```

Tente acessar um filme com censura de 14 anos e um de 13, no perfil "Infantil".

#### Proibido deletar

```python
#movie/viewsets.py
class NotDeletePermission(BasePermission):
    message = 'Nenhum registro pode ser deletado.'

    def has_permission(self, request, view):
        if request.method == 'DELETE':
            response = {
                'message': self.message,
                'status_code': status.HTTP_403_FORBIDDEN
            }
            raise DRFValidationError(response)
        else:
            return True


class MovieViewSet(viewsets.ModelViewSet):
    ...
    permission_classes = (DjangoModelPermissions, CensurePermission, NotDeletePermission)
```

