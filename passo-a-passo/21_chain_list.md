# Django Experience #21 - Chain List Queryset - Encadeando consultas

<a href="">
    <img src="../img/youtube.png">
</a>

## Problema

Eu preciso juntar todos os **filmes** e **videos** numa única lista.

Mas os filmes estão no models `Movie` e os videos no models `Video`.

## Possível solução

Antes vamos inserir alguns dados.

### Inserindo alguns dados

Primeiro vamos deletar alguns dados.

```
python manage.py shell_plus
```

```python
Movie.objects.all().delete()
Video.objects.all().delete()

titles = ['Matrix', 'Star Wars IV', 'Avengers']
movies = [Movie(title=title, rating=5, like=True, censure=14) for title in titles]
Movie.objects.bulk_create(movies)

titles = [
    ('A Essência do Django', 2021),
    ('Mini curso Entendendo Django REST framework', 2022),
    ('Django Ninja API REST', 2022),
    ('Matrix', 1999)
]
videos = [Video(title=title[0], release_year=title[1]) for title in titles]
Video.objects.bulk_create(videos)
```

### Union

Primeiro vamos tentar com [union](https://docs.djangoproject.com/en/4.0/ref/models/querysets/#union).

[https://docs.djangoproject.com/en/4.0/ref/models/querysets/#union](https://docs.djangoproject.com/en/4.0/ref/models/querysets/#union)


```python
movies = Movie.objects.values_list('title')
videos = Video.objects.values_list('title')

movies.count()

videos.count()

qs = movies.union(videos).order_by('title')
qs
```

**Obs:** Union **não** funciona no SQLite.


### itertools.chain

Então vamos tentar com [chain](https://docs.python.org/3/library/itertools.html#itertools.chain) do *itertools*.

[https://docs.python.org/3/library/itertools.html#itertools.chain](https://docs.python.org/3/library/itertools.html#itertools.chain)


```python
from itertools import chain

list(chain(movies, videos))
```

Também podemos fazer

```python
movies = Movie.objects.all()
videos = Video.objects.all()

items = list(chain(movies, videos))

for item in items:
    try:
        print(item.title, item.rating)
    except AttributeError:
        print(item.title, item.release_year)
```

Mas não é uma boa solução.

Então façamos

```python
movies = Movie.objects.values('title', 'rating')
videos = Video.objects.values('title', 'release_year')

list(chain(movies, videos))
```
