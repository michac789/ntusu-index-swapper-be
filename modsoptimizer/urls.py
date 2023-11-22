from django.urls import path
from django.http import HttpResponse
from . import views


app_name = 'modsoptimizer'
urlpatterns = [
    path('', lambda _: HttpResponse('Mods Optimizer - TODO')),
    path('scrape_course/', views.get_course_data),
    path('scrape_exam/', views.get_exam_data),
]
