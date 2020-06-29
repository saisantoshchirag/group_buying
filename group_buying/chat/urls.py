from django.urls import path,include
import django_eventstream
from . import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from dzone import settings
urlpatterns = [
    # path('',views.home),
    path('rooms/<room_id>',views.home,name='home'),
    path('rooms/<room_id>/messages',views.messages,name='message'),
    path('rooms/<room_id>/events/', include(django_eventstream.urls), {'format-channels': ['room-{room_id}']}),
    path('',views.rooms,name='rooms'),
	# older endpoint allowing client to select channel. not recommended
	path('/events/', include(django_eventstream.urls)),
    path('delete/<room>/<id>',views.delete,name='delete')
]
# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)