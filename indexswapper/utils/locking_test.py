from time import sleep
from rest_framework.decorators import api_view
from rest_framework.response import Response
from indexswapper.models import CourseIndex


@api_view(['GET'])
def locking_test_api(request):
    sleep(5)
    x = CourseIndex.objects.get(id=1)
    x.pending_count += 1
    x.save()
    return Response('ok')
