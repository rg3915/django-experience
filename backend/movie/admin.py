from django.contrib import admin

from backend.movie.models import Category, Movie


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('title',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'rating', 'censure', 'like')
    search_fields = ('title', 'sinopse', 'rating', 'like')
    list_filter = ('like', 'category')
