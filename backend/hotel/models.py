from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=32)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotéis'
