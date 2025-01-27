from django.urls import path
from .views import create_room, invite_to_room, room_detail, send_message, room_list, manage_room_users, remove_user_from_room

urlpatterns = [
    path("create/", create_room, name="create_room"),
    path("<int:room_id>/", room_detail, name="room_detail"),
    path("<int:room_id>/invite/", invite_to_room, name="invite_to_room"),
    path("<int:room_id>/send_message/", send_message, name="send_message"),
    path("", room_list, name="room_list"),
    path("room/<int:room_id>/manage-users/", manage_room_users, name="manage_room_users"),
    path("<int:room_id>/remove/<int:user_id>/", remove_user_from_room, name="remove_user_from_room"),


]
