from django.contrib.auth.models import User
from django.db import models


class Department(models.Model):
    name = models.CharField('nome', max_length=255, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return f'{self.name}'


class Employee(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='usuário',
        related_name='user_employees',
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        verbose_name='departamento',
        related_name='department_employees',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('user__first_name',)
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name or ""}'.strip()

    def __str__(self):
        return self.full_name


class Order(models.Model):
    title = models.CharField('título', max_length=255)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        verbose_name='funcionário',
        related_name='orders',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return self.title
