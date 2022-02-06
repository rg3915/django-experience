from django.contrib import admin

from backend.school.models import Class, Classroom, Grade, Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'registration')
    search_fields = ('registration', 'first_name', 'last_name')


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('title',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'note')
    search_fields = ('note',)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    exclude = ()
