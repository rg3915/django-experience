from django.contrib.auth.models import Group, User
from django.db import models


class Customer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customers'
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='seller_customers',
        null=True,
        blank=True
    )
    rg = models.CharField(max_length=10, null=True, blank=True)
    cpf = models.CharField(max_length=11, null=True, blank=True)
    cep = models.CharField(max_length=8, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('user__first_name',)
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    def __str__(self):
        return f'{self.user.get_full_name()}'


class Comission(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='comissions'
    )
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ('group__name',)
        verbose_name = 'comissão'
        verbose_name_plural = 'comissões'

    def __str__(self):
        return f'{self.group}'
