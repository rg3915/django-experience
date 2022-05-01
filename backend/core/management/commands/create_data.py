import string
from random import choice

from django.contrib.auth.models import Group, Permission, User
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


def add_permissions(group_name, permissions):
    '''
    Adiciona os grupos.
    '''
    group = Group.objects.get(name=group_name)
    permissions = Permission.objects.filter(codename__in=permissions)
    # Remove todas as permissões.
    group.permissions.clear()
    # Adiciona novas permissões.
    for perm in permissions:
        group.permissions.add(perm)


def create_users_groups_and_permissions():
    '''
    Criar alguns usuários, com grupos e permissões.
    '''

    # Cria os grupos
    groups = ['Criador', 'Editor', 'Gerente', 'Infantil']
    [Group.objects.get_or_create(name=group) for group in groups]

    # Adiciona permissões aos grupos
    add_permissions('Criador', ['add_movie'])
    add_permissions('Editor', ['add_movie', 'change_movie'])
    add_permissions('Gerente', ['add_movie', 'change_movie', 'delete_movie'])

    # Cria os usuários
    users = ['regis', 'criador', 'editor', 'gerente', 'pedrinho']

    for user in users:
        obj = User.objects.create_user(
            username=user,
            first_name=user.title(),
            email=f'{user}@email.com',
            is_staff=True,
        )
        obj.set_password('d')
        obj.save()

    # Associa os usuários aos grupos
    criador = User.objects.get(username='criador')
    editor = User.objects.get(username='editor')
    gerente = User.objects.get(username='gerente')
    pedrinho = User.objects.get(username='pedrinho')

    grupo_criador = Group.objects.get(name='Criador')
    criador.groups.clear()
    criador.groups.add(grupo_criador)

    grupo_editor = Group.objects.get(name='Editor')
    editor.groups.clear()
    editor.groups.add(grupo_editor)

    grupo_gerente = Group.objects.get(name='Gerente')
    gerente.groups.clear()
    gerente.groups.add(grupo_gerente)

    grupo_infantil = Group.objects.get(name='Infantil')
    pedrinho.groups.clear()
    pedrinho.groups.add(grupo_infantil)


class Command(BaseCommand):
    help = "Create data."

    def handle(self, *args, **options):
        # Deleta os usuários
        User.objects.exclude(username='admin').delete()

        create_persons()
        create_users_groups_and_permissions()
