from django.urls import path
from indexswapper.views import PopulateDatabaseView


app_name = 'indexswapper'
urlpatterns = [
    path('populate_db/',
         PopulateDatabaseView.as_view(), name='populate_db')
]
