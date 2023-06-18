import os
from rest_framework import serializers
from indexswapper.models import CourseIndex
from indexswapper.utils.scraper import populate_modules


class PopulateDatabaseSerializer(serializers.Serializer):
    admin_key = serializers.CharField(max_length=100)
    web_link = serializers.CharField(max_length=500)
    num_entry = serializers.IntegerField(min_value=0)

    def validate_admin_key(self, value):
        if value != os.environ.get('INDEXSWAPPER_ADMIN_KEY', '12345'):
            raise serializers.ValidationError('Invalid admin key!')
        return value

    def create(self, validated_data):
        populate_modules(
            validated_data['num_entry'], validated_data['web_link'])
        return {'message': 'Populated database successfully!'}


class CourseIndexPartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseIndex
        fields = ('id', 'code', 'name', 'index', 'pending_count',)


class CourseIndexCompleteSerializer(serializers.ModelSerializer):
    datetime_added = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S', read_only=True)
    information = serializers.CharField(write_only=True)
    information_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CourseIndex
        fields = ('id', 'code', 'name', 'index', 'datetime_added',
                  'pending_count', 'information', 'information_data',)
        read_only_fields = ('id', 'datetime_added', 'pending_count',)

    def get_information_data(self, obj):
        try:
            return obj.get_information
        except IndexError or Exception:
            return 'invalid data format'
