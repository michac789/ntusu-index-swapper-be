from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from modsoptimizer.utils.course_scraper import perform_course_scraping
from modsoptimizer.utils.exam_scraper import perform_exam_schedule_scraping


@api_view(['GET'])
def get_course_data(request):
    perform_course_scraping()
    return Response('TODO')


@api_view(['GET'])
def get_exam_data(request):
    perform_exam_schedule_scraping()
    return Response('TODO')
