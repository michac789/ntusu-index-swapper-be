from drf_yasg.utils import swagger_auto_schema
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet
from indexswapper.models import CourseIndex, SwapRequest
from indexswapper.serializers import (
    PopulateDatabaseSerializer,
    CourseIndexPartialSerializer,
    CourseIndexCompleteSerializer,
    SwapRequestCreateSerializer,
    SwapRequestListSerializer,
)
from indexswapper.utils import email
from indexswapper.utils.decorator import get_swap_request_with_id_verify, verify_cooldown
from indexswapper.utils.description import API_DESCRIPTIONS, swaprequest_qp
from indexswapper.utils.mixin import (
    CourseIndexQueryParamsMixin,
    SwapRequestQueryParamsMixin,
)
from sso.permissions import IsSuperUser


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
            # TODO - this caused ci to fail, uncomment this later!
            # email.send_swap_request_creation(request.user, serializer.data)
            # TODO: perform pairing algorithm
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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

    @swagger_auto_schema(operation_description=API_DESCRIPTIONS['swaprequest_search_another'])
    @action(methods=['patch'], detail=True)
    @get_swap_request_with_id_verify(SwapRequest.Status.WAITING)
    @verify_cooldown()
    def search_another(self, request, *args, **kwargs):
        # TODO: perform pairing algorithm
        email.send_swap_search_another(request.user, kwargs['instance'])
        return Response('ok')

    @swagger_auto_schema(operation_description=API_DESCRIPTIONS['swaprequest_mark_complete'])
    @action(methods=['patch'], detail=True)
    @get_swap_request_with_id_verify(SwapRequest.Status.WAITING)
    def mark_complete(self, request, *args, **kwargs):
        kwargs['instance'].status = SwapRequest.Status.COMPLETED
        kwargs['instance'].save()
        email.send_swap_completed(request.user, kwargs['instance'])
        return Response('ok')

    @swagger_auto_schema(operation_description=API_DESCRIPTIONS['swaprequest_cancel_swap'])
    @action(methods=['patch'], detail=True)
    @get_swap_request_with_id_verify(SwapRequest.Status.WAITING, SwapRequest.Status.SEARCHING)
    def cancel_swap(self, request, *args, **kwargs):
        if kwargs['instance'].status == SwapRequest.Status.SEARCHING:
            kwargs['instance'].delete()
        elif kwargs['instance'].status == SwapRequest.Status.WAITING:
            # TODO: perform pairing algorithm
            email.send_swap_cancel_pair(request.user, kwargs['instance'])
        else:
            return Response('Cannot cancel completed request.', status=status.HTTP_400_BAD_REQUEST)
        email.send_swap_cancel_self(request.user, kwargs['instance'])
        return Response('ok')
