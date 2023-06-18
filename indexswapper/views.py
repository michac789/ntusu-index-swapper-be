from collections import defaultdict
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from indexswapper.models import CourseIndex
from indexswapper.permissions import IsSuperUser
from indexswapper.serializers import (
    PopulateDatabaseSerializer,
    CourseIndexPartialSerializer,
    CourseIndexCompleteSerializer,
)


class PopulateDatabaseView(CreateAPIView):
    queryset = CourseIndex.objects.all()
    serializer_class = PopulateDatabaseSerializer
    permission_classes = [IsSuperUser]


class CourseIndexViewSet(ReadOnlyModelViewSet):
    queryset = CourseIndex.objects.all()
    lookup_field = 'index'

    def get_serializer_class(self):
        return (
            CourseIndexPartialSerializer if self.action == 'list'
            else CourseIndexCompleteSerializer
        )

    @action(methods=['get'], detail=False)
    def get_courses(self, *args, **kwargs):

        # TODO - not supported on sqlite, change to mysql or postgres soon!
        # instances = CourseIndex.objects.all().distinct('code')

        instances = CourseIndex.objects.values('code', 'name')
        unique_course_dict = defaultdict()
        for instance in instances:
            unique_course_dict[instance['code']] = instance['name']
        return Response([{
            'code': code, 'name': name
        } for code, name in unique_course_dict.items()])

    @action(methods=['get'], detail=False, url_name='get_indexes',
            url_path='get_indexes/(?P<course_code>[^/.]+)')
    def get_indexes_from_course(self, *args, **kwargs):
        instances = CourseIndex.objects.filter(code=kwargs['course_code'])
        return Response([{
            'index': x.index, 'pending_count': x.pending_count,
            'information': x.get_information
        } for x in instances])
