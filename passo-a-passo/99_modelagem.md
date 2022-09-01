# Django Experience #21 - Modelagem de Banco de Dados no Django

<a href="">
    <img src="../img/youtube.png">
</a>

## Leia

* [https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html](https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html)


## Ementa

Vamos falar sobre:

* OneToMany - Um pra Muitos - ForeignKey - Chave Estrangeira
* OneToOne - Um pra Um
* ManyToMany - Muitos pra Muitos
* Abstract Inheritance - Herança Abstrata
* Multi-table Inheritance - Herança Multi-tabela
* Proxy Model

* Fixtures
    * django-seed
    * jupyter notebook


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

# router.register(r'customers', CustomerViewSet, basename='customer')
# Lição de casa: completar a parte do viewsets e serializers.

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
```


## OneToMany - Um pra Muitos - ForeignKey - Chave Estrangeira

É o relacionamento onde usamos **chave estrangeira**, conhecido como **ForeignKey**.

![01_fk.png](../img/modelagem/01_fk.png)

Um **cliente** pode fazer vários **pedidos**, então para reproduzir o esquema acima, usamos o seguinte código:


```python
# bookstore/models.py
from django.db import models


class Customer(models.Model):
    first_name = models.CharField('nome', max_length=100)
    last_name = models.CharField('sobrenome', max_length=255, null=True, blank=True)  # noqa E501
    email = models.EmailField('e-mail', max_length=50, unique=True)
    active = models.BooleanField('ativo', default=True)

    class Meta:
        ordering = ('first_name',)
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name or ""}'.strip()

    def __str__(self):
        return self.full_name


STATUS = (
    ('p', 'Pendente'),
    ('a', 'Aprovado'),
    ('c', 'Cancelado'),
)


class Ordered(models.Model):
    status = models.CharField(max_length=1, choices=STATUS, default='p')
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        verbose_name='cliente',
        related_name='ordereds',
        null=True,
        blank=True
    )
    created = models.DateTimeField(
        'criado em',
        auto_now_add=True,
        auto_now=False
    )

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'ordem de compra'
        verbose_name_plural = 'ordens de compra'

    def __str__(self):
        if self.customer:
            return f'{str(self.pk).zfill(3)}-{self.customer}'

        return f'{str(self.pk).zfill(3)}'
```

```python
# bookstore/admin.py
from django.contrib import admin

from .models import Customer, Ordered


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'active')
    search_fields = ('first_name', 'last_name')
    list_filter = ('active',)


@admin.register(Ordered)
class OrderedAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'customer', 'status')
    search_fields = (
        'customer__first_name',
        'customer__last_name',
        'customer__email',
    )
    list_filter = ('status',)
    date_hierarchy = 'created'
```

```
python manage.py makemigrations
python manage.py migrate
```

### Diagrama ER

![](../img/modelagem/01_fk_er.png)


### Inserindo dados com django-seed

```
pip install django-seed
```

Edite `settings.py`

```python
# settings.py
INSTALLED_APPS = [
    ...
    'django_seed',
    ...
]
```

Gerando os dados

```
python manage.py seed bookstore --number=3
```

### ORM

```python
python manage.py shell_plus


from backend.bookstore.models import Customer, Ordered

customers = Customer.objects.all()

for customer in customers:
    print(customer)

ordereds = Ordered.objects.all()

for ordered in ordereds:
    print(ordered)
```

### PostgreSQL e pgAdmin no Docker

Vamos usar o PostgreSQL rodando no Docker.

```
docker-compose up -d
```

Podemos ver tudo pelo pgAdmin, ou

```
docker container exec -it db psql
```

#### As tabelas

```
\c db  # conecta no banco db
\dt    # mostra todas as tabelas
```

#### Os registros

```
SELECT * FROM bookstore_ordered;

id | status |        created         | customer_id 
----+--------+------------------------+-------------
  1 | p      | 1976-01-05 07:04:10+00 |           1
  2 | p      | 2021-02-09 06:08:27+00 |           3
  3 | p      | 1986-08-13 02:54:02+00 |           1
```

#### Schema

```
SELECT column_name, data_type FROM information_schema.columns WHERE TABLE_NAME = 'bookstore_ordered';
 column_name |        data_type         
-------------+--------------------------
 id          | bigint
 created     | timestamp with time zone
 customer_id | bigint
 status      | character varying
(4 rows)
```

## DBeaver e CloudBeaver

### CloudBeaver

https://github.com/dbeaver/cloudbeaver/wiki/Run-Docker-Container

https://cloudbeaver.io/doc/cloudbeaver.pdf

Edite o `docker-compose.yml`

```
  cloudbeaver:
    container_name: cloudbeaver
    image: dbeaver/cloudbeaver:latest
    volumes:
       - /var/cloudbeaver/workspace:/opt/cloudbeaver/workspace
    ports:
      - 5051:8978
    networks:
      - postgres

```

E rode

```
docker-compose up -d
```

Login e senha

```
Login: cbadmin
Pass: admin
```

### DBeaver

```
Host: localhost
Port: 5433
Database: db
Username: postgres
Password: postgres
```

### Jupyter Notebook

Para instalar o Jupyter digite

```
pip install jupyter
```

E para rodar digite

```
python manage.py shell_plus --notebook
```

Quando você tentar rodar

```
Customer.objects.all()
```

Você vai ter este erro

```
SynchronousOnlyOperation: You cannot call this from an async context - use a thread or sync_to_async.
```

Então edite o `settings.py`

```python
import os

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

```

Mas o código completo deve ser

```python
from backend.bookstore.models import Customer, Ordered
Customer.objects.all()

adam = Customer.objects.create(first_name='Adam', email='adam@email.com')
james = Customer.objects.create(first_name='James', email='james@email.com')

Customer.objects.all()

Ordered.objects.create(customer=adam)
Ordered.objects.create(customer=adam)
Ordered.objects.create(customer=james)
Ordered.objects.create(customer=james)
Ordered.objects.create(customer=james)

ordereds = Ordered.objects.all()

for ordered in ordereds:
    print(ordered)
    print(ordered.status)
    print(ordered.get_status_display())
    print(ordered.customer)
    print(ordered.customer.email)
```

Ou seja, a partir da ordem de compra conseguimos ver o cliente.

E como fazemos para a partir do cliente, ver as ordens de compra dele?

```python
adam.ordereds.all()
james.ordereds.all()
```



## OneToOne - Um pra Um

![02_one2one.png](../img/modelagem/02_one2one.png)

```python
# bookstore/models.py

METHOD_PAYMENT = (
    ('di', 'dinheiro'),
    ('de', 'débito'),
    ('cr', 'crédito'),
    ('pix', 'Pix'),
)


class Sale(models.Model):
    ordered = models.OneToOneField(
        Ordered,
        on_delete=models.CASCADE,
        verbose_name='ordem de compra'
    )
    paid = models.BooleanField('pago', default=False)
    date_paid = models.DateTimeField('data de pagamento', null=True, blank=True)
    method = models.CharField('forma de pagamento', max_length=3, choices=METHOD_PAYMENT)  # noqa E501
    deadline = models.PositiveSmallIntegerField('prazo de entrega', default=15)
    created = models.DateTimeField(
        'criado em',
        auto_now_add=True,
        auto_now=False
    )

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'venda'
        verbose_name_plural = 'vendas'

    def __str__(self):
        if self.ordered:
            return f'{str(self.pk).zfill(3)}-{self.ordered}'

        return f'{str(self.pk).zfill(3)}'
```

```python
# bookstore/admin.py
from .models import Sale


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'paid', 'date_paid', 'method', 'deadline')
    list_filter = ('paid', 'method')
    date_hierarchy = 'created'
```

![03_fk_one2one.png](../img/modelagem/03_fk_one2one.png)

```
python manage.py makemigrations
python manage.py migrate
```

![04_one2one_user_profile.png](../img/modelagem/04_one2one_user_profile.png)


```python
# core/models.py
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        verbose_name='usuário'
    )
    birthday = models.DateField('data de nascimento', null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    rg = models.CharField(max_length=10, null=True, blank=True)
    cpf = models.CharField(max_length=11, null=True, blank=True)

    class Meta:
        ordering = ('user__first_name',)
        verbose_name = 'perfil'
        verbose_name_plural = 'perfis'

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name or ""}'.strip()

    def __str__(self):
        return self.full_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
```


```python
# core/admin.py
from backend.core.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'birthday', 'linkedin', 'rg', 'cpf')
    search_fields = (
        'customer__first_name',
        'customer__last_name',
        'customer__email',
        'linkedin',
        'rg',
        'cpf'
    )
```



```
python manage.py makemigrations
python manage.py migrate
```

### Diagrama ER



**Obs:** Caso dê o **erro**

```
RelatedObjectDoesNotExist at /admin/login/

User has no profile.
```

Entre no shell e digite

```python
python manage.py shell_plus

from django.contrib.auth.models import User
from backend.core.models import Profile

users = User.objects.all()

for user in users:
    try:
        user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=user)
        profile.save()
```



## ManyToMany - Muitos pra Muitos

![06_m2m_author_book.png](../img/modelagem/06_m2m_author_book.png)

```python
# bookstore/models.py
class Author(models.Model):
    first_name = models.CharField('nome', max_length=100)
    last_name = models.CharField('sobrenome', max_length=255, null=True, blank=True)  # noqa E501

    class Meta:
        ordering = ('first_name',)
        verbose_name = 'autor'
        verbose_name_plural = 'autores'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name or ""}'.strip()

    def __str__(self):
        return self.full_name


class Book(models.Model):
    isbn = models.PositiveIntegerField(unique=True)
    title = models.CharField('título', max_length=255)
    rating = models.DecimalField('pontuação', max_digits=5, decimal_places=2, default=5)
    authors = models.ManyToManyField(
        Author,
        verbose_name='autores',
        blank=True
    )
    price = models.DecimalField('preço', max_digits=5, decimal_places=2)
    stock_min = models.PositiveSmallIntegerField(default=0)
    stock = models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(
        'criado em',
        auto_now_add=True,
        auto_now=False
    )
    modified = models.DateTimeField(
        'modificado em',
        auto_now_add=False,
        auto_now=True
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'livro'
        verbose_name_plural = 'livros'

    def __str__(self):
        return f'{self.title}'
```

```python
# bookstore/admin.py
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('first_name', 'last_name')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'isbn',
        '__str__',
        'rating',
        'price',
        'stock_min',
        'stock',
    )
    list_display_links = ('__str__',)
    search_fields = ('isbn', 'title')
```

```
python manage.py makemigrations
python manage.py migrate
```


![07_m2m_author_book_store.png](../img/modelagem/07_m2m_author_book_store.png)

```python
# bookstore/models.py
class Store(models.Model):
    name = models.CharField('nome', max_length=255)
    books = models.ManyToManyField(
        Book,
        verbose_name='livros',
        blank=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'loja'
        verbose_name_plural = 'lojas'

    def __str__(self):
        return f'{self.name}'
```

```python
# bookstore/admin.py
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('name',)
```

```
python manage.py makemigrations
python manage.py migrate
```


![08_m2m_fk.png](../img/modelagem/08_m2m_fk.png)

```python
# bookstore/models.py
class Book(models.Model):
    ...
    publisher = models.ForeignKey(
        'Publisher',
        on_delete=models.SET_NULL,
        verbose_name='editora',
        related_name='books',
        null=True,
        blank=True
    )

class Publisher(models.Model):
    name = models.CharField('nome', max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name = 'editora'
        verbose_name_plural = 'editoras'

    def __str__(self):
        return f'{self.name}'
```

```python
# bookstore/admin.py
from .models import Publisher


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('name',)
```

> Adicione `publisher` no `list_display` de `BookAdmin`.

```
python manage.py makemigrations
python manage.py migrate
```


![09_m2m_user_group.png](../img/modelagem/09_m2m_user_group.png)


## Abstract Inheritance - Herança Abstrata

![10_abstract.png](../img/modelagem/10_abstract.png)


```python
# persona/models.py
from django.db import models


class Person(models.Model):
    first_name = models.CharField('nome', max_length=100)
    last_name = models.CharField('sobrenome', max_length=255, null=True, blank=True)  # noqa E501
    email = models.EmailField('e-mail', max_length=50, unique=True)

    class Meta:
        abstract = True
        ordering = ('first_name',)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name or ""}'.strip()

    def __str__(self):
        return self.full_name


class Customer(Person):
    linkedin = models.URLField(max_length=255, null=True, blank=True)
    tags = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'


class Seller(Person):
    internal = models.BooleanField('interno', default=True)
    commission = models.DecimalField('comissão', max_digits=7, decimal_places=2, default=0)  # noqa E501

    class Meta:
        verbose_name = 'vendedor'
        verbose_name_plural = 'vendedores'

```

```python
# persona/admin.py
from django.contrib import admin

from .models import Customer, Seller


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'linkedin')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'internal', 'commission')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('internal',)

```


```
python manage.py makemigrations
python manage.py migrate
```

### TimeStampedModel

Um `abstract` muito comum é o `TimeStampedModel`.

![11_timestampedmodel.png](../img/modelagem/11_timestampedmodel.png)


```python
# core/models.py
class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        'criado em',
        auto_now_add=True,
        auto_now=False
    )
    modified = models.DateTimeField(
        'modificado em',
        auto_now_add=False,
        auto_now=True
    )

    class Meta:
        abstract = True
```

E podemos herdar, por exemplo, em `persona` nos models `Customer` e `Seller`.

```python
# persona/models.py
from backend.core.models import TimeStampedModel

class Customer(Person, TimeStampedModel):
    ...

class Seller(Person, TimeStampedModel):
    ...

```


```
python manage.py makemigrations
python manage.py migrate
```



## Multi-table Inheritance - Herança Multi-tabela

![12_mti.png](../img/modelagem/12_mti.png)

```python
# persona/models.py
class Pessoa(models.Model):
    first_name = models.CharField('nome', max_length=100)
    last_name = models.CharField('sobrenome', max_length=255, null=True, blank=True)  # noqa E501
    email = models.EmailField('e-mail', max_length=50, unique=True)

    class Meta:
        ordering = ('first_name',)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name or ""}'.strip()

    def __str__(self):
        return self.full_name


class PF(Pessoa):
    '''
    Pessoa Física.
    É um multi-table inheritance (herança multi-tabela)
    porque a classe pai não tem abstract.
    '''
    cpf = models.CharField(max_length=11, null=True, blank=True)
    rg = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name = 'Pessoa Física'
        verbose_name_plural = 'Pessoas Físicas'


class PJ(Pessoa):
    '''
    Pessoa Jurídica.
    '''
    cnpj = models.CharField(max_length=14, null=True, blank=True)
    ie = models.CharField('inscrição estadual', max_length=14, null=True, blank=True)  # noqa E501

    class Meta:
        verbose_name = 'Pessoa Jurídica'
        verbose_name_plural = 'Pessoas Jurídicas'

```


```python
# persona/admin.py
from .models import Pessoa, PF, PJ


@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(PF)
class PFAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'cpf', 'rg')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(PJ)
class PJAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'cnpj', 'ie')
    search_fields = ('first_name', 'last_name', 'email')

```

```
python manage.py makemigrations
python manage.py migrate
```


## Proxy Model

![13_proxy_model.png](../img/modelagem/13_proxy_model.png)

## Criando app expense

Vamos criar uma nova app chamada `expense`.

```
cd backend
python ../manage.py startapp expense
cd ..
```

Adicione em `INSTALLED_APPS`

```python
# settings.py
INSTALLED_APPS = [
    ...
    'backend.expense',
]
```

Edite `urls.py`

```python
# urls.py
...
path('', include('backend.expense.urls', namespace='expense')),
```

Edite `expense/apps.py`

```python
# expense/apps.py
...
name = 'backend.expense'
```

Crie `expense/urls.py`

```python
# expense/urls.py
from django.urls import include, path
from rest_framework import routers

app_name = 'expense'

router = routers.DefaultRouter()

# router.register(r'expenses', ExpenseViewSet, basename='expense')
# Lição de casa: completar a parte do viewsets e serializers.

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
```


```python
# expense/models.py
from django.db import models

from backend.core.models import TimeStampedModel

from .managers import ExpenseManager, ReceiptManager


class Financial(TimeStampedModel):
    description = models.CharField('descrição', max_length=300)
    due_date = models.DateField('data de vencimento', null=True, blank=True)
    value = models.DecimalField('valor', max_digits=7, decimal_places=2)
    paid = models.BooleanField('pago?', default=False)
    # paid_to = models.ForeignKey()

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return f'{self.description}'


class Expense(Financial):

    objects = ExpenseManager()

    class Meta:
        proxy = True
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'

    def save(self, *args, **kwargs):
        ''' Despesa é NEGATIVO. '''
        self.value = -1 * abs(self.value)
        super(Expense, self).save(*args, **kwargs)


class Receipt(Financial):

    objects = ReceiptManager()

    class Meta:
        proxy = True
        verbose_name = 'Recebimento'
        verbose_name_plural = 'Recebimentos'

    def save(self, *args, **kwargs):
        ''' Recebimento é POSITIVO. '''
        self.value = abs(self.value)
        super(Receipt, self).save(*args, **kwargs)

```

```python
# expense/managers.py
from django.db import models


class ExpenseManager(models.Manager):

    def get_queryset(self):
        return super(ExpenseManager, self).get_queryset().filter(value__lt=0)


class ReceiptManager(models.Manager):

    def get_queryset(self):
        return super(ReceiptManager, self).get_queryset().filter(value__gte=0)

```

```python
# expense/admin.py
from django.contrib import admin

from .models import Expense, Receipt


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'value', 'due_date', 'paid')
    search_fields = ('description',)
    list_filter = ('paid',)
    date_hierarchy = 'created'


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'value', 'due_date', 'paid')
    search_fields = ('description',)
    list_filter = ('paid',)
    date_hierarchy = 'created'

```


```
python manage.py makemigrations
python manage.py migrate
```
