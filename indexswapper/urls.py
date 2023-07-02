from django.urls import path
from rest_framework import routers
from indexswapper.views import (
    PopulateDatabaseView,
    CourseIndexViewSet,
    SwapRequestViewSet,
)


app_name = 'indexswapper'
router = routers.DefaultRouter()
router.register('courseindex', CourseIndexViewSet, basename='courseindex')
router.register('swaprequest', SwapRequestViewSet, basename='swaprequest')

urlpatterns = [
    path('populate_db/',
         PopulateDatabaseView.as_view(), name='populate_db')
] + router.urls
