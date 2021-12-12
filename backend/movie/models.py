from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name_plural = "Categories"


class Movie(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    sinopse = models.CharField(max_length=255, null=True, blank=True)
    rating = models.PositiveIntegerField()
    like = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} {self.sinopse} {self.rating} {self.like}"

    class Meta:
        verbose_name_plural = "Movies"
