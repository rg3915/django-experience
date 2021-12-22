# Django Experience #08 - DRF: Salvando dados extra

Considere a app `todo`. E o model `Todo`.

Agora temos os campos `created_by` e `status`.

```python
from django.contrib.auth.models import User

STATUS = (
    ('p', 'Pendente'),
    ('a', 'Aprovado'),
    ('c', 'Cancelado'),
)


class Todo(models.Model):
    task = models.CharField(max_length=50)
    is_done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    status = models.CharField(max_length=1, choices=STATUS, default='p')
```

É muito simples, basta sobreescrever o método `perform_create` em `viewsets.py`.

```python
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, status='a')
```


## Salvando os dados

Abra o Postman e faça um POST **logado** com `Basic Auth`.

```
{
    "task": "Tarefa aprovada"
}
```

O resultado será

```
{
    "id": 60,
    "task": "Tarefa aprovada",
    "is_done": false,
    "created": "2021-12-21T23:15:53.259852-03:00",
    "status": "a",
    "created_by": 1
}
```

Se quiser ver o usuário expandido, basta colocar `depth = 1` em `TodoSerializer`.


Leia [https://simpleisbetterthancomplex.com/tutorial/2019/04/07/how-to-save-extra-data-to-a-django-rest-framework-serializer.html
](https://simpleisbetterthancomplex.com/tutorial/2019/04/07/how-to-save-extra-data-to-a-django-rest-framework-serializer.html
)
