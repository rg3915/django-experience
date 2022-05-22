# Django Experience #21 - Modelagem de Banco de Dados no Django

<a href="">
    <img src="../img/youtube.png">
</a>

## Leia

* [https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html](https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html)


## Criando uma nova app

Vamos criar uma nova app chamada `bookstore`.

```
cd backend
python ../manage.py startapp bookstore
cd ..
```

Adicione em `INSTALLED_APPS`

```python
# settings.py
INSTALLED_APPS = [
    ...
    'backend.bookstore',
]
```

Edite `urls.py`

```python
# urls.py
...
path('', include('backend.bookstore.urls', namespace='bookstore')),
```

Edite `bookstore/apps.py`

```python
# bookstore/apps.py
...
name = 'backend.bookstore'
```

Crie `bookstore/urls.py`

```python
# bookstore/urls.py
from django.urls import include, path
from rest_framework import routers

app_name = 'bookstore'

router = routers.DefaultRouter()

# router.register(r'books', BookViewSet, basename='book')
# Lição de casa: completar a parte do viewsets e serializers.

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
```

## Criando app persona

Vamos criar uma nova app chamada `persona`.

```
cd backend
python ../manage.py startapp persona
cd ..
```

Adicione em `INSTALLED_APPS`

```python
# settings.py
INSTALLED_APPS = [
    ...
    'backend.persona',
]
```

Edite `urls.py`

```python
# urls.py
...
path('', include('backend.persona.urls', namespace='persona')),
```

Edite `persona/apps.py`

```python
# persona/apps.py
...
name = 'backend.persona'
```

Crie `persona/urls.py`

```python
# persona/urls.py
from django.urls import include, path
from rest_framework import routers

app_name = 'persona'

router = routers.DefaultRouter()

# router.register(r'customers', CustomerViewSet, basename='customer)
# Lição de casa: completar a parte do viewsets e serializers.

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
```


## OneToMany - Um pra Muitos - Foreign Key - Chave Estrangeira

![01_fk.png](../img/modelagem/01_fk.png)


## OneToOne - Um pra Um

![02_one2one.png](../img/modelagem/02_one2one.png)
![03_fk_one2one.png](../img/modelagem/03_fk_one2one.png)
![04_one2one_user_profile.png](../img/modelagem/04_one2one_user_profile.png)
![05_all.png](../img/modelagem/05_all.png)


## ManyToMany - Muitos pra Muitos

![06_m2m_author_book.png](../img/modelagem/06_m2m_author_book.png)
![07_m2m_author_book_store.png](../img/modelagem/07_m2m_author_book_store.png)
![08_m2m_fk.png](../img/modelagem/08_m2m_fk.png)
![09_m2m_user_group.png](../img/modelagem/09_m2m_user_group.png)


## Abstract Inheritance - Herança Abstrata

![10_abstract.png](../img/modelagem/10_abstract.png)
![11_timestampedmodel.png](../img/modelagem/11_timestampedmodel.png)


## Multi-table Inheritance - Herança Multi-tabela

![12_mti.png](../img/modelagem/12_mti.png)


## Proxy Model

![13_proxy_model.png](../img/modelagem/13_proxy_model.png)

