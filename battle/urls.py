from django.urls import path
from battle import views
from websocket.urls import websocket

urlpatterns = [
	path("", views.index_view),
	websocket("ws/", views.websocket_view),
	path("<chat_id>/", views.index_view),
	websocket("ws/<chat_id>/", views.websocket_view),
]