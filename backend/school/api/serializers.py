from rest_framework import serializers

from backend.school.models import Class, Classroom, Grade, Student


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'


class StudentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name')


class StudentRegistrationSerializer(serializers.BaseSerializer):

    class Meta:
        model = Student

    def to_representation(self, instance):
        return {
            'registration': instance.registration.zfill(7),
            'full_name': instance.__str__()
        }


class ClassroomSerializer(serializers.ModelSerializer):
    # students = serializers.ListSerializer(child=StudentSerializer())
    # students = StudentSerializer(many=True)
    students = serializers.ListSerializer(child=StudentSerializer(), required=False)

    class Meta:
        model = Classroom
        fields = '__all__'
        depth = 1


class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = '__all__'


class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = '__all__'


class ClassAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = ('classroom',)
