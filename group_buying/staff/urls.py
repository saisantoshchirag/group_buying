from django.urls import path, include
from . import views

app_name = 'staff'
urlpatterns = [
    path('confirm/',views.confirm,name='confirm')
]