from rest_framework import serializers
from modsoptimizer.models import CourseCode, CourseIndex


class CourseCodePartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCode
        fields = [
            'id',
            'code',
            'name',
            'academic_units',
        ]


class CourseIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseIndex
        fields = [
            'id',
            'index',
            'get_information',
            'schedule'
        ]


class CourseCodeSerializer(serializers.ModelSerializer):
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


class CourseOptimizerInputSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    include = serializers.ListField(child=serializers.CharField(max_length=5), required=False)
    exclude = serializers.ListField(child=serializers.CharField(max_length=5), required=False)
    
    def validate_code(self, value):
        # course code must exist
        if not CourseCode.objects.filter(code=value).exists():
            raise serializers.ValidationError(f'Course code `{value}` does not exist.')
        return value
    
    def validate(self, data):
        # include and exclude list should contain indexes that exist for the course code
        for li in [data.get('include', []), data.get('exclude', [])]:
            for index in li:
                if index not in data['code'].indexes.values_list('index', flat=True):
                    raise serializers.ValidationError(f'Index `{index}` does not exist for course `{data["code"]}`.')
        return data


class OptimizerInputSerialzer(serializers.Serializer):
    courses = CourseOptimizerInputSerializer(many=True)
    occupied = serializers.RegexField(regex=r'^[OX]{192}$', required=False)
