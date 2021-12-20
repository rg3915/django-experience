# Django Experience #05 - DRF: Serializers mais rápido

Baseado em [https://hakibenita.com/django-rest-framework-slow](https://hakibenita.com/django-rest-framework-slow)

Editar `settings.py`

```python
# settings.py

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5000
}
```

Editar `movie/models.py`

```python
# movie/models.py
class Movie(models.Model):
    ...

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'sinopse': self.sinopse,
            'rating': self.rating,
            'like': self.like,
            'created': self.created,
            # 'category': self.category.id,
        }

```

Editar `movie/api/serializers.py`

```python
# movie/api/serializers.py
class MovieReadOnlySerializer(serializers.ModelSerializer):
    # category = CategorySerializer(required=False)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'sinopse', 'rating', 'like', 'created')
        read_only_fields = fields

```

Editar `movie/api/viewsets.py`

```python
# movie/api/viewsets.py
class MovieViewSet(viewsets.ModelViewSet):
    ...

    @action(detail=False, methods=['get'])
    def movies_readonly(self, request, pk=None):
        movies = Movie.objects.all()

        page = self.paginate_queryset(movies)
        if page is not None:
            serializer = MovieReadOnlySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = MovieReadOnlySerializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def movies_regular_readonly(self, request, pk=None):
        movies = Movie.objects.all()

        page = self.paginate_queryset(movies)
        if page is not None:
            serializer = [movie.to_dict() for movie in page]
            return self.get_paginated_response(serializer)

        serializer = [movie.to_dict() for movie in movies]
        return Response(serializer)

```

Editar `client.py`

```python
# client.py
import timeit

import requests

base_url = 'http://localhost:8000/api/v1'

url_video = f'{base_url}/videos/'
url_movie = f'{base_url}/movies/?format=json'
url_movie_readonly = f'{base_url}/movies/movies_readonly/?format=json'
url_movie_regular_readonly = f'{base_url}/movies/movies_regular_readonly/?format=json'


def get_result(url):
    start_time = timeit.default_timer()
    r = requests.get(url)
    print('status_code:', r.status_code)
    end_time = timeit.default_timer()
    print('time:', round(end_time - start_time, 3))
    print()


if __name__ == '__main__':
    get_result(url_video)
    get_result(url_movie)
    get_result(url_movie_readonly)
    get_result(url_movie_regular_readonly)
```

Rodando...

```
pip install requests
python client.py
```

Resultado:

```
status_code: 200
time: 0.114

status_code: 200
time: 4.969

status_code: 200
time: 0.504

status_code: 200
time: 0.151
```
