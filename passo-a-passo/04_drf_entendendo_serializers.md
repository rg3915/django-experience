# Django Experience #04 - DRF: Entendendo Serializers

Doc: [Serializers](https://www.django-rest-framework.org/api-guide/serializers/)

Basicamente, serialização é quando você transforma uma estrutura de dados num formato que possa ser transmitido pela rede e reconstruído posteriormente no mesmo ou em outro ambiente.

Ou seja, transforma objetos Python (JSON) em string.

A desserialização transforma a string em objeto Python novamente.

Continuando com nossa app `movie`, temos:


## Declarando um Serializers

```python
from rest_framework import serializers

from backend.movie.models import Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=30)
    sinopse = serializers.CharField(max_length=255)
    rating = serializers.IntegerField()
    like = serializers.BooleanField(default=False)
```

Abra o `shell` do Django.

```
python manage.py shell_plus
```

Primeiro vamos criar um filme.

```python
from backend.movie.api.serializers import MovieSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from backend.movie.models import Movie

movie = Movie(
    title='Matrix',
    sinopse='Filme de ficção',
    rating=5,
    like=True
)
```

### Serialização

Agora podemos ver a serialização da última instância.

```python
In [5]: serializer = MovieSerializer(movie)

In [6]: serializer.data
Out[6]: {'title': 'Matrix', 'sinopse': 'Filme de ficção', 'rating': 5, 'like': True}
```

Neste ponto nós traduzimos a instância do modelo em tipos de dados nativos do Python. Para finalizar o processo de serialização nós vamos renderizar os dados em uma string no formato `json`.


```python
In [7]: content = JSONRenderer().render(serializer.data)

In [8]: content
Out[8]: b'{"title":"Matrix","sinopse":"Filme de fic\xc3\xa7\xc3\xa3o","rating":5,"like":true}'
```


### Desserialização

A desserialização é similar.

```python
import io
from rest_framework.parsers import JSONParser

# content foi definido acima
stream = io.BytesIO(content)
data = JSONParser().parse(stream)

serializer = MovieSerializer(data=data)

In [11]: serializer.is_valid()
Out[11]: True

In [12]: serializer.validated_data
Out[12]: 
OrderedDict([('title', 'Matrix'),
             ('sinopse', 'Filme de ficção'),
             ('rating', 5),
             ('like', True)])
```


## Salvando a instância

```python
class MovieSerializer(serializers.Serializer):
    ...

    def create(self, validated_data):
        """
        Create and return a new `Movie` instance, given the validated data.
        Cria e retorna uma nova instância `Movie`, de acordo com os dados validados.
        :param validated_data:
        """
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Movie` instance, given the validated data.
        Atualiza e retorna uma instância `Movie` existente, de acordo com os dados validados.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.sinopse = validated_data.get('sinopse', instance.sinopse)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.like = validated_data.get('like', instance.like)
        instance.save()
        return instance
```

Agora podemos fazer

```
python manage.py shell_plus
```

Agora podemos chamar o método `save()` para retornar a instância do objeto, baseado no `validated_data`.

```python
movie = serializer.save()
```

E ainda:

```python
from backend.movie.api.serializers import MovieSerializer
from backend.movie.models import Movie

data = {'title': 'Vingadores Ultimato', 'sinopse': 'Filme de super-heróis', 'rating': 5, 'like': True}
serializer = MovieSerializer(data=data)
serializer.data
```

Erro

```
AssertionError: When a serializer is passed a `data` keyword argument you must call `.is_valid()` before attempting to access the serialized `.data` representation.
You should either call `.is_valid()` first, or access `.initial_data` instead.
```

```python
serializer.is_valid()
serializer.data

# agora tente salvar
serializer.save()
```

Erro

```
AssertionError: You cannot call `.save()` after accessing `serializer.data`. If you need to access data before committing to the database then inspect 'serializer.validated_data' instead. 
```

```python
from backend.movie.api.serializers import MovieSerializer
from backend.movie.models import Movie

data = {'title': 'Vingadores Ultimato', 'sinopse': 'Filme de super-heróis', 'rating': 5, 'like': True}
serializer = MovieSerializer(data=data)

# AssertionError: You must call `.is_valid()` before calling `.save()`.

serializer.is_valid()
serializer.save()
```

## Validação simples e Atualização parcial

Agora vamos atualizar os dados.

```python
from backend.movie.api.serializers import MovieSerializer
from backend.movie.models import Movie

movie = Movie.objects.get(title='Vingadores Ultimato')
data = {'sinopse': 'Após Thanos eliminar metade das criaturas vivas, os Vingadores têm de lidar com a perda de amigos e entes queridos. Com Tony Stark vagando perdido no espaço sem água e comida, Steve Rogers e Natasha Romanov lideram a resistência contra o titã louco.'}
serializer = MovieSerializer(movie, data=data)
serializer.is_valid()  # False

serializer.errors
Out[11]: {'title': [ErrorDetail(string='Este campo é obrigatório.', code='required')], 'rating': [ErrorDetail(string='Este campo é obrigatório.', code='required')]}

serializer = MovieSerializer(movie, data=data, partial=True)
serializer.is_valid()  # True
serializer.save()
```

## Objetos aninhados (nested objects)

Doc: [Dealing with nested objects](https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects)

Acrescente uma chave estrangeira no models `Movie`:

```python
class Movie(models.Model):
    ...
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        verbose_name='categoria',
        related_name='movies',
        null=True,
        blank=True
    )
```

```python
from backend.movie.api.serializers import MovieSerializer
from backend.movie.models import Movie

movie = Movie.objects.last()
serializer = MovieSerializer(movie)
serializer.data
```

### Gravando uma representação aninhada

```
python manage.py shell_plus
```

```python
from backend.movie.api.serializers import MovieSerializer
from backend.movie.models import Movie

data={'category': {'title': 'Ação'}, 'title': 'Vingadores Guerra Infinita', 'sinopse': 'Filme de super-heróis', 'rating': 5, 'like': True}
serializer = MovieSerializer(data=data)
serializer.is_valid()
serializer.save()
```

Erro

```
ValueError: Cannot assign "OrderedDict([('title', 'Ação')])": "Movie.category" must be a "Category" instance.
```

Então vamos editar o `serializers.py`.

```python
class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=30)


class MovieSerializer(serializers.Serializer):
    ...
    category = CategorySerializer()

    def create(self, validated_data):
        """
        Create and return a new `Movie` instance, given the validated data.
        Cria e retorna uma nova instância `Movie`, de acordo com os dados validados.
        :param validated_data:
        """
        category_data = {}
        if 'category' in validated_data:
            category_data = validated_data.pop('category')

        if category_data:
            category = Category.objects.create(**category_data)
            movie = Movie.objects.create(category=category, **validated_data)
        else:
            movie = Movie.objects.create(**validated_data)

        return movie
```

Agora podemos tentar novamente

```
python manage.py shell_plus
```

```python
from backend.movie.api.serializers import MovieSerializer
from backend.movie.models import Movie

data={'category': {'title': 'Ação'}, 'title': 'Vingadores Guerra Infinita', 'sinopse': 'Filme de super-heróis', 'rating': 5, 'like': True}
serializer = MovieSerializer(data=data)
serializer.is_valid()
serializer.save()
```

Agora vamos editar o `update`.

```python
# serializers.py
class MovieSerializer(serializers.Serializer):
    ...

    def update(self, instance, validated_data):
        """
        Update and return an existing `Movie` instance, given the validated data.
        Atualiza e retorna uma instância `Movie` existente, de acordo com os dados validados.
        """
        if 'category' in validated_data:
            category_data = validated_data.pop('category')
            title = category_data.get('title')
            category, _ = Category.objects.get_or_create(title=title)
            # Atualiza a categoria
            instance.category = category

        # Atualiza a instância
        instance.title = validated_data.get('title', instance.title)
        instance.sinopse = validated_data.get('sinopse', instance.sinopse)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.like = validated_data.get('like', instance.like)
        instance.save()

        return instance
```

Agora podemos editar

```
python manage.py shell_plus
```

```python
from backend.movie.api.serializers import MovieSerializer
from backend.movie.models import Movie

movie = Movie.objects.get(title='Vingadores Guerra Infinita')
data={'category': {'title': 'Ação'}, 'title': 'Vingadores Guerra Infinita', 'sinopse': 'Filme de super-heróis', 'rating': 6, 'like': True}
serializer = MovieSerializer(movie, data=data, partial=True)
serializer.is_valid()
serializer.save()
```

A esse ponto nós já esquecemos do jeito mais simples, então vamos escrever o `create()` e o `update()` de `CategorySerializer`.

```python
# serializers.py
class CategorySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=30)

    def create(self, validated_data):
        """
        Create and return a new `Category` instance, given the validated data.
        Cria e retorna uma nova instância `Category`, de acordo com os dados validados.
        :param validated_data:
        """
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Category` instance, given the validated data.
        Atualiza e retorna uma instância `Category` existente, de acordo com os dados validados.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance
```


### Lista de objetos

```python
from backend.movie.api.serializers import MovieSerializer
from backend.movie.models import Movie

queryset = Movie.objects.all()
serializer = MovieSerializer(queryset, many=True)
serializer.data

from rest_framework.renderers import JSONRenderer
from pprint import pprint

json = JSONRenderer().render(serializer.data)
pprint(json)
```

Mais dois exemplos:

```python
from backend.movie.api.serializers import MovieSerializer
from backend.movie.models import Movie

movie = Movie.objects.get(title='Matrix')
data={'rating': 5}
serializer = MovieSerializer(movie, data=data, partial=True)
serializer.is_valid()
serializer.save()
serializer.data
```


```python
from backend.movie.api.serializers import MovieSerializer
from backend.movie.models import Movie

movie = Movie.objects.get(title='Matrix')
data={'category': {'title': 'Drama'}, 'rating': 2}
serializer = MovieSerializer(movie, data=data, partial=True)
serializer.is_valid()
serializer.save()
serializer.data
```

## ModelSerializer

Doc: [ModelSerializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer)


```python
# movie/serializers.py
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'title')
```

```python
>>> from backend.movie.api.serializers import CategorySerializer

>>> serializer = CategorySerializer()
>>> print(repr(serializer))

CategorySerializer():
    id = IntegerField(label='ID', read_only=True)
    title = CharField(max_length=30, validators=[<UniqueValidator(queryset=Category.objects.all())>])
```

> Rode os testes.


```python
# movie/serializers.py
class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'sinopse', 'rating', 'like', 'category')
```

```
python manage.py shell_plus
```

```python
from backend.movie.api.serializers import MovieSerializer
from backend.movie.models import Movie

In [2]: data={'category': {'title': 'Ação'}, 'title': 'Vingadores Guerra Infinita', 'sinopse': 'Filme de super-heróis', '
   ...: rating': 5, 'like': True}
   ...: 

In [3]: serializer = MovieSerializer(data=data)
   ...: 

In [4]: serializer.is_valid()
   ...: 
Out[4]: False

In [5]: serializer.errors
Out[5]: {'category': [ErrorDetail(string='Tipo incorreto. Esperado valor pk, recebeu dict.', code='incorrect_type')]}
```

Então acrescente `depth = 1` em `MovieSerializer`.

```python
# movie/serializers.py
class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'sinopse', 'rating', 'like', 'category')
        depth = 1
```

```
python manage.py shell_plus
```

```python
from backend.movie.api.serializers import MovieSerializer
from backend.movie.models import Movie

data={'category': {'title': 'Ação'}, 'title': 'Vingadores Guerra Infinita', 'sinopse': 'Filme de super-heróis', 'rating': 5, 'like': True}
serializer = MovieSerializer(data=data)
serializer.is_valid()
serializer.save()
serializer.data
```

Só que ele não salvou a categoria. Então

```python
# movie/serializers.py
class MovieSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'sinopse', 'rating', 'like', 'category')

    def create(self, validated_data):
        """
        Create and return a new `Movie` instance, given the validated data.
        Cria e retorna uma nova instância `Movie`, de acordo com os dados validados.
        :param validated_data:
        """
        category_data = {}
        if 'category' in validated_data:
            category_data = validated_data.pop('category')

        if category_data:
            category, _ = Category.objects.get_or_create(**category_data)
            movie = Movie.objects.create(category=category, **validated_data)
        else:
            movie = Movie.objects.create(**validated_data)

        return movie

    def update(self, instance, validated_data):
        """
        Update and return an existing `Movie` instance, given the validated data.
        Atualiza e retorna uma instância `Movie` existente, de acordo com os dados validados.
        """
        if 'category' in validated_data:
            category_data = validated_data.pop('category')
            title = category_data.get('title')
            category, _ = Category.objects.get_or_create(title=title)
            # Atualiza a categoria
            instance.category = category

        # Atualiza a instância
        instance.title = validated_data.get('title', instance.title)
        instance.sinopse = validated_data.get('sinopse', instance.sinopse)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.like = validated_data.get('like', instance.like)
        instance.save()

        return instance
```

```
python manage.py shell_plus
```

```python
from backend.movie.api.serializers import MovieSerializer
from backend.movie.models import Movie

data={'category': {'title': 'Ação'}, 'title': 'Matrix Reloaded', 'sinopse': 'Filme de ação', 'rating': 5, 'like': True}
serializer = MovieSerializer(data=data)
serializer.is_valid()

# serializer.errors

serializer.save()
serializer.data
```

> Rode os testes.


## ListSerializer

Doc: [https://www.django-rest-framework.org/api-guide/serializers/#listserializer](https://www.django-rest-framework.org/api-guide/serializers/#listserializer)

Vamos criar uma nova app chamado `school`

```
python manage.py dr_scaffold school Student \
registration:charfield \
first_name:charfield \
last_name:charfield

python manage.py dr_scaffold school Classroom \
title:charfield \
students:ManyToMany:Student
```

```python
# school/models.py
from django.db import models


class Student(models.Model):
    registration = models.CharField(max_length=7)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"


class Classroom(models.Model):
    title = models.CharField(max_length=30)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Sala de aula"
        verbose_name_plural = "Salas de aula"
```

```python
# school/serializers.py
from rest_framework import serializers

from backend.school.models import Classroom, Student


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'


class ClassroomSerializer(serializers.ModelSerializer):
    students = serializers.ListSerializer(child=StudentSerializer())

    class Meta:
        model = Classroom
        fields = '__all__'
```

Ou simplesmente `many=True`.

```python
class ClassroomSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)

    class Meta:
        model = Classroom
        fields = '__all__'
```

Ou simplesmente `depth = 1`.

```python
class ClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = '__all__'
        depth = 1
```

## BaseSerializer

Doc: [https://www.django-rest-framework.org/api-guide/serializers/#baseserializer](https://www.django-rest-framework.org/api-guide/serializers/#baseserializer)

```python
# school/serializers.py
class StudentRegistrationSerializer(serializers.BaseSerializer):

    class Meta:
        model = Student

    def to_representation(self, instance):
        return {
            'registration': instance.registration.zfill(7),
            'full_name': instance.__str__()
        }
```

```python
# school/views.py
from rest_framework.decorators import action
from rest_framework.response import Response


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=False, methods=['get'])
    def all_students(self, request, pk=None):
        queryset = Student.objects.all()
        serializer = StudentRegistrationSerializer(queryset, many=True)
        return Response(serializer.data)

```
