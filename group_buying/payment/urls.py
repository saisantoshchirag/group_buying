from django.urls import path,include
from django.conf.urls import url
from . import views
# app_name = 'home'
app_name = 'payment'
urlpatterns = [
    path('pay/',views.payment_home,name='home'),
    path("checkout/", views.checkout, name="Checkout"),
    path("payment/", views.app_create,name="payment"),
    path("payment/charge/", views.app_charge,name="charge")

]
