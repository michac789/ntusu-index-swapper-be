from django.urls import path
from django.http import HttpResponse


app_name = 'modsoptimizer'
urlpatterns = [
    path('', lambda _: HttpResponse('Mods Optimizer - TODO')),
]
