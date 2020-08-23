from django.urls import path,include
from django.conf.urls import url
from . import views
# app_name = 'home'
app_name = 'payment'
urlpatterns = [
    path('pay/',views.payment_home,name='home')
]
