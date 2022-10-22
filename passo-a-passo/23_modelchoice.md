# Django Experience #23 - ModelChoiceField

<a href="https://youtu.be/zzspqykDfic">
    <img src="../img/youtube.png">
</a>

## Criando dados para os Pedidos

```
python manage.py seed order --number=15
```


```
python manage.py shell_plus
```


```python
from random import choice


Department.objects.all().delete()
Employee.objects.all().delete()
Order.objects.all().delete()

departments = ('Vendas', 'Financeiro', 'RH')
objs = [Department(name=name) for name in departments]
Department.objects.bulk_create(objs)


users = User.objects.exclude(username='admin')

for user in users:
    user.username = user.first_name.lower()
    user.email = f'{user.first_name.lower()}@example.net'
    user.is_staff = True
    user.save()

departments = Department.objects.all()

for user in users:
    Employee.objects.create(department=choice(departments), user=user)
```

## O formulário

```python
from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    required_css_class = 'required'

    employee = forms.ModelChoiceField(
        label='Funcionário',
        queryset=None,
    )

    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Retorna o funcionário logado.
        employee = user.user_employees.first()

        # Retorna o departamento do funcionário logado.
        department = employee.department

        # Retorna somente os funcionários do meu departamento.
        employees = Employee.objects.filter(department=department)

        # Altera o filtro de ModelChoiceField.
        self.fields['employee'].queryset = employees

        # Adiciona classe form-control nos campos.
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

```

## A views

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import OrderForm
from .models import Order


def order_list(request):
    template_name = 'order/order_list.html'
    object_list = Order.objects.all()
    context = {'object_list': object_list}
    return render(request, template_name, context)


@login_required
def order_create(request):
    template_name = 'order/order_form.html'
    # Passa o usuário logado no formulário.
    form = OrderForm(request.user, request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('order:order_list')

    context = {'form': form}
    return render(request, template_name, context)

```
