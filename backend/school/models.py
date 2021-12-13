from django.db import models


class Student(models.Model):
    registration = models.CharField(max_length=7)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"


class Classroom(models.Model):
    title = models.CharField(max_length=30)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Sala de aula"
        verbose_name_plural = "Salas de aula"
