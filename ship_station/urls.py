from django.urls import path
from .views import model_form_upload


app_name = 'ship_station'


urlpatterns = [
    path('qty_finder/',model_form_upload,name='qty_finder'),
]