from django.http import Http404
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
from indexswapper.utils.mixin import CourseIndexQueryParamsMixin


class PopulateDatabaseView(CreateAPIView):
    queryset = CourseIndex.objects.all()
    serializer_class = PopulateDatabaseSerializer
    permission_classes = [IsSuperUser]


class CourseIndexViewSet(CourseIndexQueryParamsMixin,
                         ReadOnlyModelViewSet):
    queryset = CourseIndex.objects.all()
    lookup_field = 'index'

    def get_serializer_class(self):
        return (
            CourseIndexPartialSerializer if self.action == 'list'
            else CourseIndexCompleteSerializer
        )

    @action(methods=['get'], detail=False)
    def get_courses(self, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        unique_courses = qs.values('code', 'name').distinct()
        page = self.paginate_queryset(unique_courses)
        return self.get_paginated_response(page)

    @action(methods=['get'], detail=False,
            url_path='get_indexes/(?P<course_code>[^/.]+)')
    def get_indexes_from_course(self, *args, **kwargs):
        qs = CourseIndex.objects.filter(code=kwargs['course_code'])
        if qs.count() == 0:
            raise Http404()
        return Response([{
            'index': x.index, 'pending_count': x.pending_count,
            'information': x.get_information
        } for x in qs])
