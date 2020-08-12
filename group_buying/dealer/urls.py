from django.urls import path,include
from . import views
app_name='dealer'
urlpatterns = [
    path('status',views.status,name='status'),
    path('upload',views.upload,name='upload'),
    path('current',views.current,name='current'),
    path('update',views.update,name='update')
]