# Django Experience #15 - DRF: Entendendo Validações


Doc: https://www.django-rest-framework.org/api-guide/validators/

Podemos fazer a validação por cada campo, ou pelo modelo em geral.

```python
# movie/api/serializers.py
class MovieSerializer(serializers.ModelSerializer):
    ...

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'sinopse',
            'rating',
            'censure',
            'like',
            'created',
            'category'
        )

    def validate_title(self, value):
        if 'lorem' in value.lower():
            raise serializers.ValidationError('Lorem não pode.')
        return value

    def validate(self, data):
        if 'lorem' in data['title'].lower():
            raise serializers.ValidationError('Lorem não pode.')
        return data
```

Um outro exemplo interessante é a comparação entra datas.

Considere a app `Hotel`.

```python
# hotel/models.py
from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=32)
    start_date = models.DateField(null=True, blank=True)  # ou checkin
    end_date = models.DateField(null=True, blank=True)  # ou checkout
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotéis'
```

```python
# hotel/api/viewsets.py
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from backend.hotel.api.serializers import HotelSerializer
from backend.hotel.models import Hotel


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = (AllowAny,)
```

```python
# hotel/api/serializers.py
from rest_framework import serializers

from backend.hotel.models import Hotel


class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = '__all__'

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('A data inicial deve ser anterior ou igual a data inicial!')
        return data
```



https://www.django-rest-framework.org/api-guide/fields/#integerfield

Temos também as validações específicas de cada campo.

```python
# movie/api/serializers.py
class MovieSerializer(serializers.ModelSerializer):
    censure = serializers.IntegerField(min_value=0)
```

## Custom Validators (Validações Customizadas)

Também podemos criar nossas próprias customizações.

```python
# movie/api/serializers.py
def positive_only_validator(value):
    if value == 0:
        raise serializers.ValidationError('Zero não é um valor permitido.')


class MovieSerializer(serializers.ModelSerializer):
    censure = serializers.IntegerField(min_value=0, validators=[positive_only_validator])
```
