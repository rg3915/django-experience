# Django Experience #17 - Novo comando

<a href="https://youtu.be/ag6zD1JbeLI">
    <img src="../img/youtube.png">
</a>

Vamos criar um comando para criar novos clientes.

```
python manage.py create_command core -n create_data
```

```python
# core/management/commands/create_data.py
import string
from random import choice

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from backend.crm.models import Customer

fake = Faker()


def gen_digits(max_length):
    return str(''.join(choice(string.digits) for i in range(max_length)))


def gen_email(first_name: str, last_name: str):
    first_name = slugify(first_name)
    last_name = slugify(last_name)
    email = f'{first_name}.{last_name}@email.com'
    return email


def get_person():
    name = fake.first_name()
    username = name.lower()
    first_name = name
    last_name = fake.last_name()
    email = gen_email(first_name, last_name)

    user = User.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email
    )

    data = dict(
        user=user,
        rg=gen_digits(9),
        cpf=gen_digits(11),
        cep=gen_digits(8),
    )
    return data


def create_persons():
    aux_list = []
    for _ in range(6):
        data = get_person()
        obj = Customer(**data)
        aux_list.append(obj)
    Customer.objects.bulk_create(aux_list)


class Command(BaseCommand):
    help = 'Create data.'

    def handle(self, *args, **options):
        create_persons()

```

