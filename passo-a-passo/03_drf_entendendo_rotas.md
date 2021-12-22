# Django Experience #03 - DRF: Entendendo Rotas

Doc: [Routers](https://www.django-rest-framework.org/api-guide/routers/)

Vamos criar uma app chamada `movie` usando o [dr_scaffold]().

```
python manage.py dr_scaffold movie Movie \
title:charfield \
sinopse:charfield \
rating:positiveintegerfield \
like:booleanfield

python manage.py dr_scaffold movie Category title:charfield
```


Não se esqueça de adicionar `movie` em `INSTALLED_APPS`.


## SimpleRouter

Basicamente você precisa informar `prefix` e `viewset` na rota.

```python
# movie/urls.py
from django.urls import include, path
from rest_framework import routers

from movie.views import CategoryViewSet, MovieViewSet

router = routers.SimpleRouter()

# router.register(prefix, viewset)
router.register(r'movies', MovieViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
```


O `basename` é requerido quando você altera o `queryset` original, exemplo:

```python
# movie/views.py
class MovieViewSet(viewsets.ModelViewSet):
    # queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_queryset(self):
        return Movie.objects.filter(title__icontains='lorem')
```

Erro:

```
AssertionError: `basename` argument not specified, and could not automatically determine the name from the viewset, as it does not have a `.queryset` attribute.
```

Então defina

```python
# movie/urls.py
router.register(r'movies', MovieViewSet, basename="movie")
router.register(r'categories', CategoryViewSet, basename="category")
```

Por fim teremos as rotas:

```
URL                         Nome
/movie/categories/          category-list
/movie/categories/<pk>/     category-detail
/movie/movies/              movie-list
/movie/movies/<pk>/         movie-detail
```

O `basename` é usado para especificar a parte inicial do nome da view.


### Rota extra

Em edite `views.py`

```python
# movie/views.py
class MovieViewSet(viewsets.ModelViewSet):
    # queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_queryset(self):
        return Movie.objects.filter(title__icontains='lorem')

    @action(detail=False, methods=['get'])
    def get_good_movies(self, request, pk=None):
        '''
        Retorna somente filmes bons, com rating maior ou igual a 4.
        '''
        movies = Movie.objects.filter(rating__gte=4)

        page = self.paginate_queryset(movies)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)
```

Acabamos de ganhar uma sub-rota

```
/movie/movies/get_good_movies/    movie-get-good-movies
```

Ler [https://www.django-rest-framework.org/api-guide/routers/#simplerouter](https://www.django-rest-framework.org/api-guide/routers/#simplerouter)



## DefaultRouter

Este é semelhante ao `SimpleRouter`. A única diferença é que ele te oferece um formato de saída na rota, exemplo em `json`.

```python
# movie/urls.py
router = routers.DefaultRouter()
```


Exemplo:

```
http://localhost:8000/movie/movies/?format=json
```

