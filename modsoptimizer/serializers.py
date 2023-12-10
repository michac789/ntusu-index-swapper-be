from rest_framework.serializers import ModelSerializer
from modsoptimizer.models import CourseCode, CourseIndex


class CourseCodePartialSerializer(ModelSerializer):
    class Meta:
        model = CourseCode
        fields = [
            'id',
            'code',
            'name',
            'academic_units',
        ]


class CourseIndexSerializer(ModelSerializer):
    class Meta:
        model = CourseIndex
        fields = [
            'id',
            'index',
            'get_information',
            'schedule'
        ]


class CourseCodeSerializer(ModelSerializer):
    indexes = CourseIndexSerializer(many=True, read_only=True)
    
    class Meta:
        model = CourseCode
        fields = [
            'id',
            'code',
            'name',
            'academic_units',
            'datetime_added',
            'get_exam_schedule',
            'indexes',
        ]
