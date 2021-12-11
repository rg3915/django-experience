from django.contrib import admin

from backend.todo.models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_done')
    search_fields = ('task',)
    list_filter = ('is_done',)
    date_hierarchy = 'created'
