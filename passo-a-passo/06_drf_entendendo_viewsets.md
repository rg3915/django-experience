# Django Experience #06 - DRF: Entendendo Viewsets

Doc: [Viewsets](https://www.django-rest-framework.org/api-guide/viewsets/)

## ViewSets

https://www.django-rest-framework.org/api-guide/viewsets/

Vamos considerar a app `school`.

Crie um arquivo `school/viewsets.py`.

```python
# school/viewsets.py
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from backend.school.models import Student
from backend.school.api.serializers import StudentRegistrationSerializer, StudentSerializer


class StudentViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving students.
    Uma ViewSet simples para listar ou recuperar alunos.
    """

    def list(self, request):
        queryset = Student.objects.all()
        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Student.objects.all()
        student = get_object_or_404(queryset, pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

```

Edite `school/urls.py`.

```python
# school/urls.py
from django.urls import include, path
from rest_framework import routers

from school.views import ClassroomViewSet
from school.viewsets import StudentViewSet as SimpleStudentViewSet

router = routers.DefaultRouter()

router.register(r'students', SimpleStudentViewSet)
router.register(r'classrooms', ClassroomViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
```

Erro:

```python
assert queryset is not None, '`basename` argument not specified, and could ' \
AssertionError: `basename` argument not specified, and could not automatically determine the name from the viewset, as it does not have a `.queryset` attribute.
```

Então defina o `basename`.

```python
...
router.register(r'students', SimpleStudentViewSet, basename='student')
...
```

### Nova rota com action

```python
# school/viewsets.py
...
from rest_framework.decorators import action
from rest_framework.response import Response

class StudentViewSet(viewsets.ViewSet):
    ...

    @action(detail=False, methods=['get'])
    def all_students(self, request, pk=None):
        queryset = Student.objects.all()
        serializer = StudentRegistrationSerializer(queryset, many=True)
        return Response(serializer.data)

```

### Todas as ações do ViewSet implementadas explicitamente

Primeiro momento

```python
# school/viewsets.py
class StudentViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving students.
    Uma ViewSet simples para listar ou recuperar alunos.
    """

    def get_serializer_class(self):
        pass

    def get_serializer(self, *args, **kwargs):
        pass

    def get_queryset(self):
        pass

    def get_object(self):
        pass

    def list(self, request):
        queryset = Student.objects.all()
        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        queryset = Student.objects.all()
        student = get_object_or_404(queryset, pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
```

Se você definir `get_serializer()` diretamente...

```python
    def get_serializer(self):
        return StudentSerializer
```

... vai dar o seguinte erro:

`AttributeError: 'property' object has no attribute 'copy'`

Então defina

```python
    def get_serializer_class(self):
        return StudentSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)
```

Então podemos reescrever o método `list()`

```python
    def list(self, request):
        # queryset = Student.objects.all()
        # serializer = StudentSerializer(queryset, many=True)
        # return Response(serializer.data)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        # Sem paginação
        return Response(serializer.data)

```

Completo

```python
# school/viewsets.py
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.school.models import Student
from backend.school.api.serializers import StudentRegistrationSerializer, StudentSerializer


class StudentViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving students.
    Uma ViewSet simples para listar ou recuperar alunos.
    """

    def get_serializer_class(self):
        return StudentSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        queryset = Student.objects.all()
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(queryset, pk=pk)
        return obj

    def list(self, request):
        # queryset = Student.objects.all()
        # serializer = StudentSerializer(queryset, many=True)
        # return Response(serializer.data)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        # Sem paginação
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        queryset = Student.objects.all()
        student = get_object_or_404(queryset, pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, pk=None):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def all_students(self, request, pk=None):
        queryset = Student.objects.all()
        serializer = StudentRegistrationSerializer(queryset, many=True)
        return Response(serializer.data)
```


## GenericViewSet

https://www.django-rest-framework.org/api-guide/generic-views/

Edite `school/serializers.py`


```python
# school/serializers.py
class ClassroomSerializer(serializers.ModelSerializer):
    students = serializers.ListSerializer(child=StudentSerializer(), required=False)
```

Edite `school/viewsets.py`

```python
# school/viewsets.py
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny

from backend.school.models import Classroom, Student
from backend.school.api.serializers import (
    ClassroomSerializer,
    StudentRegistrationSerializer,
    StudentSerializer
)

class ClassroomSerializer(generics.ListCreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = (AllowAny,)
```


## ModelViewSet

https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset

```python
# school/viewsets.py
class ClassroomSerializer(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = (AllowAny,)
```


## ReadOnlyModelViewSet

https://www.django-rest-framework.org/api-guide/viewsets/#readonlymodelviewset


Vamos criar mais um model.

```
python manage.py dr_scaffold school Grade \
student:foreignkey:Student \
note:decimalfield
```

Edite `school/models.py`

```python
# school/models.py
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    note = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0.0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} {self.note}"

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"
```

Edite `school/viewsets.py`

```python
# school/viewsets.py
from backend.school.models import Classroom, Grade, Student
from backend.school.api.serializers import (
    ClassroomSerializer,
    GradeSerializer,
    StudentRegistrationSerializer,
    StudentSerializer
)

class GradeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = (AllowAny,)
```

Edite `school/urls.py`

```python
# school/urls.py
from school.viewsets import GradeViewSet
```

```
python manage.py makemigrations
python manage.py migrate
```


## Entendendo os métodos do ModelViewSet

https://www.cdrf.co/

### get_serializer_class

Usado para escolher qual serializer você quer usar dependendo de determinadas condições.

**Exemplo:** Suponha que você queira cadastrar um aluno, mas ao editar você só pode alterar o nome e sobrenome.

Então vamos criar dois serializers.

```python
# school/serializers.py
class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'


class StudentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name')
```

E em `school/viewsets.py`

```python
# school/viewsets.py
class StudentViewSet(viewsets.ViewSet):

    def get_serializer_class(self):
        # Muda o serializer dependendo da ação.
        if self.action == 'create':
            return StudentSerializer

        if self.action == 'update':
            return StudentUpdateSerializer

        return StudentSerializer
```

### list

Suponha que eu queira ver somente os meus alunos.

Primeiro vamos editar alguns arquivos:

```python
# school/models.py
from django.contrib.auth.models import User

class Class(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.classroom} {self.teacher}"

    class Meta:
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"
```


```python
# school/admin.py
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    exclude = ()
```


```python
# school/serializers.py
class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = '__all__'
        # depth = 1  # com ele você não consegue fazer um POST direto pelo browser do Django.
```


```python
# school/viewsets.py
class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
```


```python
# school/urls.py
from school.viewsets import ClassViewSet, GradeViewSet

router.register(r'class', ClassViewSet)
```

#### Editando ClassViewSet

Voltemos ao arquivo `school/viewsets.py`

```python
# school/viewsets.py
class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user
        teacher = User.objects.get(username=user)

        if user is not None:
            queryset = Class.objects.filter(teacher=teacher)
        else:
            queryset = Class.objects.none()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
```

### get_queryset

Talvez modificar o queryset padrão já seja suficiente.

```python
# school/viewsets.py
class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    # def list(self, request, *args, **kwargs):
    #     ...

    def get_queryset(self):
        user = self.request.user
        teacher = User.objects.get(username=user)

        if user is not None:
            queryset = Class.objects.filter(teacher=teacher)
        else:
            queryset = Class.objects.none()
        return queryset
```


### perform_create

Usado quando você quiser mudar o comportamento de como seu objeto é criado.

Vamos editar

```python
# school/serializers.py
class ClassAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = ('classroom',)
```

```python
# school/viewsets.py
class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    # serializer_class = ClassSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return ClassAddSerializer

        if self.action == 'update':
            return ClassSerializer

        return ClassSerializer

    def perform_create(self, serializer):
        user = self.request.user
        teacher = User.objects.get(username=user)

        if user is not None:
            serializer.save(teacher=teacher)
```


### create

Usado quando você quiser mudar a resposta. Exemplo, adicionar dados extras na resposta, etc.

Leia também [Quando usar o create () do Serializer e o create () perform_create () do ModelViewset](https://qastack.com.br/programming/41094013/when-to-use-serializers-create-and-modelviewsets-create-perform-create)

Direto de [ModelViewSet.html#create](https://www.cdrf.co/3.12/rest_framework.viewsets/ModelViewSet.html#create) temos:

```python
# school/viewsets.py
class ClassViewSet(viewsets.ModelViewSet):
    ...

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
```

### perform_update

Usado quando você quiser mudar o comportamento de como seu objeto é editado.

Ex: https://www.codegrepper.com/code-examples/python/django+rest+model+viewset+standard+update

```python
# school/viewsets.py
class ClassViewSet(viewsets.ModelViewSet):
    ...

    >>> REVISAR REVISAR REVISAR REVISAR REVISAR REVISAR REVISAR REVISAR REVISAR REVISAR REVISAR REVISAR REVISAR REVISAR REVISAR REVISAR 

    def perform_update(self, serializer):
        user = self.request.user
        data = self.request.data
        teacher_id = data.get('teacher')

        try:
            teacher = User.objects.get(pk=teacher_id)
        except User.DoesNotExist:
            raise DRFValidationError('Usuário não encontrado.')

        if user and user.is_authenticated:
            if user == teacher:
                serializer.save()
            else:
                raise DRFValidationError('Você não tem permissão para esta operação.')
```

Vamos experimentar pelo Postman.

Faça autenticação em `Authorization -> Basic Auth`, logando como `admin`.

```
http://localhost:8000/school/class/1/
PUT

{
    "classroom": 5,
    "teacher": 1
}
```

### retrieve

Pega apenas uma instância do objeto.

```python
# school/viewsets.py
class ClassViewSet(viewsets.ModelViewSet):
    ...

    def retrieve(self, request, *args, **kwargs):
        '''
        Método para ver os detalhes.
        '''
        instance = self.get_object()
        teacher = instance.teacher
        user = self.request.user

        if user and user.is_authenticated:
            if user == teacher:
                serializer = self.get_serializer(instance)
            else:
                raise DRFValidationError('Você não tem acesso a esta aula.')

        return Response(serializer.data)
```

### delete

Ex: Deletar somente os seus dados.

Ou não deletar nada.

```python
# school/viewsets.py
class ClassViewSet(viewsets.ModelViewSet):
    ...

    def perform_destroy(self, instance):
        '''
        Método para deletar os dados.
        '''
        # instance.delete()
        raise DRFValidationError('Nenhuma aula pode ser deletada.')
```


### Remover o delete da rota

```python
from rest_framework.generics import GenericAPIView 
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin

class BookViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericAPIView
)
```

Repare que não temos o `DestroyModelMixin`.

Ilustrações

https://testdriven.io/blog/drf-views-part-3/

