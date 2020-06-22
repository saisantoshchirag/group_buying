from django.urls import path,include
from django.conf.urls import url
from . import views
# app_name = 'home'

urlpatterns = [
    # path('update',)
    path('update',views.update,name='update'),
    path('editprofile',views.city,name='edit'),
    path('view/',views.profile,name='view'),

]
