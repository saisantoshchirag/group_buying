# from django.conf.urls import url
from channels.routing import URLRouter
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
import django_eventstream
from django.urls import path
urlpatterns = [
	path('rooms/<room_id>/events/', AuthMiddlewareStack(
		URLRouter(django_eventstream.routing.urlpatterns)
	), {'format-channels': ['room-{room_id}']}),

	# older endpoint allowing client to select channel. not recommended
	path('events/', AuthMiddlewareStack(
		URLRouter(django_eventstream.routing.urlpatterns)
	)),

	path(r'', AsgiHandler),
]