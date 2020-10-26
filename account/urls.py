from django.urls import path 
from .views import registration_view



app_name = 'account' 

urlpatterns = [
    path('register/', registration_view, name='registration_view'),
    #path('password/', change_password, name='change_password'),
] 
    