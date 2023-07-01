import os
from django.core.validators import MinLengthValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from indexswapper.models import CourseIndex, SwapRequest
from indexswapper.utils.scraper import populate_modules


class PopulateDatabaseSerializer(serializers.Serializer):
    admin_key = serializers.CharField(max_length=100)
    web_link = serializers.CharField(max_length=500)
    num_entry = serializers.IntegerField(min_value=0)

    def validate_admin_key(self, value):
        if value != os.environ.get('INDEXSWAPPER_ADMIN_KEY', '12345'):
            raise serializers.ValidationError('Invalid admin key!')
        return value

    def save(self):
        populate_modules(
            self.validated_data['num_entry'],
            self.validated_data['web_link'],
        )
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


class SwapRequestCreateSerializer(serializers.ModelSerializer):
    current_index_num = serializers.CharField(max_length=5, write_only=True)
    wanted_indexes = serializers.ListField(
        child=serializers.CharField(max_length=5),
        validators=[MinLengthValidator(1)])

    class Meta:
        model = SwapRequest
        fields = ('contact_info', 'current_index_num', 'wanted_indexes')

    def create(self, validated_data):
        validated_data['current_index'] = CourseIndex.objects.get(
            index=validated_data['current_index_num'])
        del validated_data['current_index_num']
        return super().create(validated_data)

    def validate(self, data):
        instance = get_object_or_404(
            CourseIndex,
            index=data['current_index_num'])
        for index in data['wanted_indexes']:
            try:
                curr_courseindex = CourseIndex.objects.get(index=index)
            except CourseIndex.DoesNotExist:
                raise serializers.ValidationError(
                    f'Bad request, wanted index {index} does not exist')
            if curr_courseindex.index == instance.index:
                raise serializers.ValidationError(
                    f'Bad request, wanted index {index} cannot be the same as current index')
            if curr_courseindex.code != instance.code:
                raise serializers.ValidationError(
                    f'Bad request, wanted index {index} ({curr_courseindex.code}) should be the same course code with current index {index} ({instance.code})')
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['course_code'] = instance.current_index.code
        data['course_name'] = instance.current_index.name
        data['current_index'] = instance.current_index.index
        data['id'] = instance.id
        return data


class SwapRequestListSerializer(serializers.ModelSerializer):
    datetime_added = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    datetime_found = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    wanted_indexes = serializers.SerializerMethodField()
    current_index = serializers.SerializerMethodField()

    class Meta:
        model = SwapRequest
        fields = '__all__'

    def get_wanted_indexes(self, obj):
        try:
            return eval(obj.wanted_indexes)
        except:
            return obj.wanted_indexes

    def get_current_index(self, obj):
        return obj.current_index.index
