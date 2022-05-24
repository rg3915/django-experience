# Generated by Django 4.0.4 on 2022-05-23 03:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='nome')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='sobrenome')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='e-mail')),
                ('active', models.BooleanField(default=True, verbose_name='ativo')),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
                'ordering': ('first_name',),
            },
        ),
        migrations.CreateModel(
            name='Ordered',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='p', max_length=1)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordereds', to='bookstore.customer', verbose_name='cliente')),
            ],
            options={
                'verbose_name': 'ordem de compra',
                'verbose_name_plural': 'ordens de compra',
                'ordering': ('-pk',),
            },
        ),
    ]
