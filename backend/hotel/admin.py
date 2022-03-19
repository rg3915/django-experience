from django.contrib import admin

from backend.hotel.models import Hotel


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'start_date',
        'end_date',
        'created'
    )
    search_fields = ('name',)
    date_hierarchy = 'created'
    ordering = ('-created',)
