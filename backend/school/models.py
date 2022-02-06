from django.contrib.auth.models import User
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


class Class(models.Model):
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name='classes',
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_classes',
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.classroom} {self.teacher}"

    class Meta:
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"


class Grade(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='grades',
        null=True,
        blank=True,
    )
    note = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        default=0.0
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} {self.note}"

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"
