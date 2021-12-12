from django.contrib import admin

from backend.movie.models import Category, Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    exclude = ()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ()
