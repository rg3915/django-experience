from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy

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

    def __str__(self):
        return f"{self.task}"

    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"

    def get_absolute_url(self):
        return reverse_lazy('todo:todo_detail', kwargs={'pk': self.pk})
