from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from modsoptimizer.utils.exam_scraper import perform_exam_schedule_scraping


@api_view(['GET'])
def exam_schedule_scraper(request):
    perform_exam_schedule_scraping()
    return Response('TODO')
