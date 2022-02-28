from django.contrib import admin

from backend.example.models import Example


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    exclude = ()
