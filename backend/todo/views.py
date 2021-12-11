from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)

from .forms import TodoForm
from .models import Todo


class TodoListView(ListView):
    model = Todo
    paginate_by = 10


class TodoDetailView(DetailView):
    model = Todo


class TodoCreateView(CreateView):
    model = Todo
    form_class = TodoForm


class TodoUpdateView(UpdateView):
    model = Todo
    form_class = TodoForm


class TodoDeleteView(DeleteView):
    model = Todo
    success_url = reverse_lazy('todo:todo_list')
