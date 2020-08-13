from django.urls import path, include
from . import views

app_name = 'staff'
urlpatterns = [
    path('confirm/',views.confirm,name='confirm'),
    path('updatestauts/<user_id>/<status>',views.update_status,name='update_status')
]