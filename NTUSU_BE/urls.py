"""
URL configuration for NTUSU_BE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title='NTUSU ITC BACKEND API',
        default_version='1.0.0',
        description='Automatic Documentation, Easily use the API here!',
    ), public=True
)

urlpatterns = [
    path('', lambda _: HttpResponse('NTUSU ITC BACKEND')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger')),

    path('indexswapper/', include('indexswapper.urls')),
    path('modsoptimizer/', include('modsoptimizer.urls')),
    path('sso/', include('sso.urls')),
]
