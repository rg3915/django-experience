from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    list_display = (
        '__str__',
        'email',
        'first_name',
        'last_name',
        'get_groups',
        'is_staff',
        'is_superuser',
    )

    @admin.display(description='Grupos')
    def get_groups(self, obj):
        groups = obj.groups.all()
        if groups:
            return ', '.join([group.name for group in groups])


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
