from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet
from indexswapper.models import CourseIndex, SwapRequest
from indexswapper.permissions import IsSuperUser
from indexswapper.serializers import (
    PopulateDatabaseSerializer,
    CourseIndexPartialSerializer,
    CourseIndexCompleteSerializer,
    SwapRequestCreateSerializer,
    SwapRequestListSerializer,
)
from indexswapper.utils.description import API_DESCRIPTIONS, swaprequest_qp
from indexswapper.utils.mixin import (
    CourseIndexQueryParamsMixin,
    SwapRequestQueryParamsMixin,
)


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


swaprequest_qp = openapi.Parameter(
    'status', openapi.IN_QUERY,
    description="filter status with 'S' (searching),'W' (waiting), 'C' (completed))",
    type=openapi.TYPE_STRING)


class SwapRequestViewSet(SwapRequestQueryParamsMixin,
                         ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=SwapRequestCreateSerializer,
        operation_description=API_DESCRIPTIONS['swaprequest_create'],
    )
    def create(self, request):
        serializer = SwapRequestCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            # TODO: send email to user
            # TODO: perform pairing algorithm
            return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[swaprequest_qp],
        operation_description=API_DESCRIPTIONS['swaprequest_list']
    )
    def list(self, request):
        queryset = SwapRequest.objects.filter(user=request.user.id)
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        serializer = SwapRequestListSerializer(queryset, many=True)
        return Response(serializer.data)
