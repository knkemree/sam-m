from django.urls import path
from .views import model_form_upload
from ship_station.views import lookup, update_source_file


app_name = 'ship_station'


urlpatterns = [
    path('update_source_file/',update_source_file,name='update_source_file'),
    path('lookup/',lookup,name='lookup'),
]