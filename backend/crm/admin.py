from django.contrib import admin

from .models import Comission, Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'rg', 'cpf', 'cep', 'seller', 'active')
    list_display_links = ('__str__',)
    search_fields = (
        'user__first_name',
        'user__last_name',
        'user__email',
        'seller__first_name',
        'seller__last_name',
        'seller__email',
        'rg',
        'cpf',
        'cep',
        'address',
    )
    list_filter = ('active',)


@admin.register(Comission)
class ComissionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'percentage')
