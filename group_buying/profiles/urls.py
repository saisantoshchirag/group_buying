from django.urls import path,include
from django.conf.urls import url
from . import views
# app_name = 'home'

urlpatterns = [
    # path('update',)
    path('update',views.update,name='update'),
    path('view/',views.profile,name='view'),
    path('create/',views.create,name='create')
]