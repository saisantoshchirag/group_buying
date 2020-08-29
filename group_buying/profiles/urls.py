from django.urls import path,include
from django.conf.urls import url
from . import views
# app_name = 'home'

urlpatterns = [
    # path('update',)
    path('update',views.update,name='update'),
    path('view/<name>',views.profile,name='view'),
    path('create/',views.create,name='create'),
    path('phone',views.phone_number,name='phone_number'),
    path('change',views.change_phone,name='change_phone'),
    path('otp',views.validate_otp,name='otp'),
    path('verify',views.verify_phone,name='verify_phone')
]
