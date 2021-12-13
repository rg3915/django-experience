from rest_framework import serializers

from backend.school.models import Classroom, Student


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'

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

    class Meta:
        model = Classroom
        fields = '__all__'
        depth = 1
