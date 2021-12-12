from django.db import models


class Video(models.Model):
    title = models.CharField('título', max_length=50, unique=True)
    release_year = models.PositiveIntegerField('lançamento', null=True, blank=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'filme'
        verbose_name_plural = 'filmes'

    def __str__(self):
        return f'{self.title}'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year,
        }
