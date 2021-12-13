from django.contrib import admin

from backend.school.models import Class, Classroom, Grade, Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    exclude = ()


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    exclude = ()


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    exclude = ()


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    exclude = ()
