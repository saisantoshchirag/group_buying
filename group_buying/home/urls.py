from django.urls import path,include   
from django.conf.urls import url
from . import views
# app_name = 'home'

urlpatterns = [
    path('',views.home,name='home')
]
