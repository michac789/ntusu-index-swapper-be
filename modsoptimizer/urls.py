from django.urls import path
from django.http import HttpResponse
from modsoptimizer.utils import exam_scraper
from . import views


app_name = 'modsoptimizer'
urlpatterns = [
    path('', lambda _: HttpResponse('Mods Optimizer - TODO')),
    path('scrape/', views.exam_schedule_scraper),
]
