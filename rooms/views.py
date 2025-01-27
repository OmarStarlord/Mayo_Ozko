import pusher
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Message
from .forms import RoomForm, InviteUserForm
from django.contrib.auth import get_user_model
from django.db import transaction
import pusher
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
import json
import logging




logger = logging.getLogger(__name__)




User = get_user_model()

# Initialize Pusher client
pusher_client = pusher.Pusher(
    app_id='1931997',
    key='b47d20482e4df2bf538c',
    secret='e280f4c8b43ecfff83b4',
    cluster='eu',
    ssl=True
)

@login_required
def create_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.moderator = request.user
            room.save()
            room.users.add(request.user)  # Auto-add creator to the room
            messages.success(request, f"Room '{room.name}' created successfully!")
            return redirect("room_detail", room_id=room.id)
    else:
        form = RoomForm()
    return render(request, "rooms/create_room.html", {"form": form})

@login_required
def invite_to_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.user != room.moderator:
        messages.error(request, "Only the room moderator can invite users.")
        return redirect("room_detail", room_id=room.id)

    if request.method == "POST":
        form = InviteUserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            room.users.add(user)
            messages.success(request, f"{user.username} has been invited to '{room.name}'.")
            return redirect("room_detail", room_id=room.id)
    else:
        form = InviteUserForm()

    return render(request, "rooms/invite_to_room.html", {"form": form, "room": room})

@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    messages = room.messages.all().order_by("timestamp")
    return render(request, "rooms/room_detail.html", {"room": room, "messages": messages})


@login_required
@require_http_methods(["POST"])
def send_message(request, room_id):
    try:
        # Validate and parse JSON data
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        # Validate message content
        message_content = data.get('message', '').strip()
        if not message_content:
            return JsonResponse({"error": "Message cannot be empty"}, status=400)
        if len(message_content) > 2000:  # Match your TextField requirements
            return JsonResponse({"error": "Message too long (max 2000 characters)"}, status=400)

        # Validate room and permissions
        room = get_object_or_404(Room, id=room_id)
        if not room.users.filter(id=request.user.id).exists():
            return JsonResponse({"error": "You are not a member of this room"}, status=403)

        # Create and save message
        try:
            message = Message.objects.create(
                room=room,
                sender=request.user,
                content=message_content
            )
        except Exception as e:
            logger.error(f"Message creation failed: {str(e)}")
            return JsonResponse({"error": "Message creation failed"}, status=500)

        # Pusher notification with error handling
        try:
            pusher_client.trigger(
                f'chat_{room_id}',
                'new_message',
                {
                    'sender': message.sender.username,
                    'message': message.content,
                    'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                }
            )
        except Exception as e:
            logger.error(f"Pusher notification failed: {str(e)}")
            # Continue even if Pusher fails

        return JsonResponse({
            "status": "success",
            "message": {
                "id": message.id,
                "content": message.content,
                "timestamp": message.timestamp.isoformat()
            }
        })

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return JsonResponse({"error": "Internal server error"}, status=500)



@login_required
def room_list(request):
    # Get all rooms the user is part of
    rooms = Room.objects.filter(users=request.user)
    return render(request, "rooms/room_list.html", {"rooms": rooms})

@login_required
def manage_room_users(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.user != room.moderator:
        messages.error(request, "Only the room moderator can manage users.")
        return redirect("room_detail", room_id=room.id)

    users_in_room = room.users.all()

    return render(request, "rooms/manage_users.html", {"room": room, "users": users_in_room})

@login_required
def remove_user_from_room(request, room_id, user_id):
    room = get_object_or_404(Room, id=room_id)
    user_to_remove = get_object_or_404(User, id=user_id)

    if request.user != room.moderator:
        messages.error(request, "Only the room moderator can remove users.")
        return redirect("manage_room_users", room_id=room.id)

    if user_to_remove == room.moderator:
        messages.error(request, "You cannot remove yourself as the moderator.")
    else:
        room.users.remove(user_to_remove)
        messages.success(request, f"{user_to_remove.username} has been removed from the room.")

    return redirect("manage_room_users", room_id=room.id)
