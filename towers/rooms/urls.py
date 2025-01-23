from django.urls import path
from .views import create_room, invite_to_room, room_detail, send_message, room_list

urlpatterns = [
    path("create/", create_room, name="create_room"),
    path("<int:room_id>/", room_detail, name="room_detail"),
    path("<int:room_id>/invite/", invite_to_room, name="invite_to_room"),
    path("<int:room_id>/send_message/", send_message, name="send_message"),
    path("", room_list, name="room_list"),
]
