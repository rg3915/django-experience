from django.db import models
from django.urls import reverse_lazy


class Todo(models.Model):
    task = models.CharField(max_length=50)
    is_done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task}"

    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"

    def get_absolute_url(self):
        return reverse_lazy('todo:todo_detail', kwargs={'pk': self.pk})
