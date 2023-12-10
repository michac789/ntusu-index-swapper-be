from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from modsoptimizer.models import CourseCode
from modsoptimizer.serializers import CourseCodePartialSerializer, CourseCodeSerializer
from modsoptimizer.utils.course_scraper import perform_course_scraping
from modsoptimizer.utils.exam_scraper import perform_exam_schedule_scraping
from modsoptimizer.utils.mixin import CourseCodeQueryParamsMixin


@api_view(['GET'])
def get_course_data(request):
    perform_course_scraping()
    return Response('Scraping Completed')


@api_view(['GET'])
def get_exam_data(request):
    perform_exam_schedule_scraping()
    return Response('Scraping Completed')


class CourseCodeListView(CourseCodeQueryParamsMixin, ListAPIView):
    serializer_class = CourseCodePartialSerializer
    queryset = CourseCode.objects.all()


class CourseCodeDetailView(RetrieveAPIView):
    serializer_class = CourseCodeSerializer
    lookup_field = 'course_code'
    
    def get_object(self):
        return CourseCode.objects.get(code=self.kwargs['course_code'])
