# Django Experience #02 - Criando API com Django SEM DRF - parte 2

```
cd backend
python ../manage.py startapp video
cd ..
```


Edite `settings.py`

```python
INSTALLED_APPS = [
    ...
    'backend.video',
]
```

Edite `video/apps.py`

```python
# video/apps.py
name = 'backend.video'
```

Edite `video/models.py`

```python
# video/models.py
from django.db import models


class Video(models.Model):
    title = models.CharField('título', max_length=50, unique=True)
    release_year = models.PositiveIntegerField('lançamento', null=True, blank=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'filme'
        verbose_name_plural = 'filmes'

    def __str__(self):
        return f'{self.title}'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year,
        }

```

Edite `video/admin.py`

```python
# video/admin.py
from django.contrib import admin

from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'release_year')
    search_fields = ('title',)

```


```
python manage.py makemigrations
python manage.py migrate
```


Edite `video/forms.py`

```python
# video/forms.py
from django import forms

from .models import Video


class VideoForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = ('title', 'release_year')

```

Edite `video/views.py`

```python
import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .forms import VideoForm
from .models import Video


@csrf_exempt
def videos(request):
    '''
    Lista ou cria videos.
    '''
    videos = Video.objects.all()
    data = [video.to_dict() for video in videos]
    form = VideoForm(request.POST or None)

    if request.method == 'POST':
        if request.POST:
            # Dados obtidos pelo formulário.
            if form.is_valid():
                video = form.save()

        elif request.body:
            # Dados obtidos via json.
            data = json.loads(request.body)
            video = Video.objects.create(**data)

        else:
            return JsonResponse({'message': 'Algo deu errado.'})

        return JsonResponse({'data': video.to_dict()})

    return JsonResponse({'data': data})


@csrf_exempt
def video(request, pk):
    '''
    Mostra os detalhes, edita ou deleta um video.
    '''
    video = get_object_or_404(Video, pk=pk)
    form = VideoForm(request.POST or None, instance=video)

    if request.method == 'GET':
        data = video.to_dict()
        return JsonResponse({'data': data})

    if request.method == 'POST':
        if request.POST:
            # Dados obtidos pelo formulário.
            if form.is_valid():
                video = form.save()

        elif request.body:
            # Dados obtidos via json.
            data = json.loads(request.body)

            for attr, value in data.items():
                setattr(video, attr, value)
            video.save()

        else:
            return JsonResponse({'message': 'Algo deu errado.'})

        return JsonResponse({'data': video.to_dict()})

    if request.method == 'DELETE':
        video.delete()
        return JsonResponse({'data': 'Item deletado com sucesso.'})

```

Edite `video/urls.py`

```python
# video/urls.py
from django.urls import include, path

from backend.video import views as v

app_name = 'video'

v1_urlpatterns = [
    path('videos/', v.videos, name='videos'),
    path('videos/<int:pk>/', v.video, name='video'),
]

urlpatterns = [
    path('api/v1/', include(v1_urlpatterns)),
]

```

Edite `backend/urls.py`

```python
# backend/urls.py
urlpatterns = [
    ...
    path('', include('backend.video.urls', namespace='video')),
]
```


Edite `nav.html`

```python
<!-- nav.html -->
<li class="nav-item">
  <a class="nav-link" href="{% url 'video:videos' %}">API V1 Video</a>
</li>
```

Edite `video/tests.py`

```python
# video/tests.py
import json

from django.test import TestCase

from .models import Video


class VideoTest(TestCase):

    def setUp(self):
        self.payload = {
            "title": "Matrix",
            "release_year": 1999
        }

    def test_video_create(self):
        response = self.client.post(
            '/api/v1/videos/',
            data=self.payload,
            content_type='application/json'
        )
        resultado = json.loads(response.content)
        esperado = {
            "data": {
                "id": 1,
                **self.payload
            }
        }
        self.assertEqual(esperado, resultado)

    def test_video_list(self):
        Video.objects.create(**self.payload)

        response = self.client.get(
            '/api/v1/videos/',
            content_type='application/json'
        )
        resultado = json.loads(response.content)
        esperado = {
            "data": [
                {
                    "id": 1,
                    **self.payload
                }
            ]
        }
        self.assertEqual(esperado, resultado)

    def test_video_detail(self):
        Video.objects.create(**self.payload)

        response = self.client.get(
            '/api/v1/videos/1/',
            content_type='application/json'
        )
        resultado = json.loads(response.content)
        esperado = {
            "data": {
                "id": 1,
                **self.payload
            }
        }
        self.assertEqual(esperado, resultado)

    def test_video_update(self):
        Video.objects.create(**self.payload)

        data = {
            "title": "Matrix 2"
        }

        response = self.client.post(
            '/api/v1/videos/1/',
            data=data,
            content_type='application/json'
        )
        resultado = json.loads(response.content)
        esperado = {
            "data":
            {
                "id": 1,
                "title": "Matrix 2",
                "release_year": 1999
            }
        }
        self.assertEqual(esperado, resultado)

    def test_video_delete(self):
        Video.objects.create(**self.payload)

        response = self.client.delete(
            '/api/v1/videos/1/',
            content_type='application/json'
        )
        resultado = json.loads(response.content)
        esperado = {"data": "Item deletado com sucesso."}

        self.assertEqual(esperado, resultado)

```

