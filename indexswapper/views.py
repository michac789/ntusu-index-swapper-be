from collections import defaultdict
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from indexswapper.models import CourseIndex
from indexswapper.serializers import PopulateDatabaseSerializer
from indexswapper.utils.scraper import populate_modules


class PopulateDatabaseView(GenericAPIView):
    serializer_class = PopulateDatabaseSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            populate_modules(
                serializer.validated_data['num_entry'],
                serializer.validated_data['web_link']
            )
            return Response({
                'success': 'Population completed!',
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CourseIndexViewSet(ViewSet):
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
