from django.urls import path,include
import django_eventstream
from . import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from dzone import settings
urlpatterns = [
    path('rooms/<room_id>',views.home,name='home'),
    path('rooms/<room_id>/messages',views.messages,name='message'),
    path('rooms/<room_id>/events/', include(django_eventstream.urls), {'format-channels': ['room-{room_id}']}),
    path('',views.rooms,name='rooms'),
    path('/events/', include(django_eventstream.urls)),
    path('delete/<room>/<id>',views.delete,name='delete'),
    path('data',views.data),
    path('join/<room_id>',views.join,name='join')
]
