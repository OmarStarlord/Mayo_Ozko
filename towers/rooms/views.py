from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Message
from .forms import RoomForm, InviteUserForm
from django.contrib.auth import get_user_model

User = get_user_model()

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
            return redirect("rooms/room_detail", room_id=room.id)
    else:
        form = RoomForm()
    return render(request, "rooms/create_room.html", {"form": form})

@login_required
def invite_to_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.user != room.moderator:
        messages.error(request, "Only the room moderator can invite users.")

        # Redirect back to the room detail page
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
    return render(request, "rooms/room_detail.html", {"room": room, "messages": room.messages.all()})

@login_required
def send_message(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Message.objects.create(room=room, sender=request.user, content=content)
            # WebSockets will handle live updates later
            return redirect("room_detail", room_id=room.id)

    return redirect("rooms/room_detail", room_id=room.id)


@login_required
def room_list(request):
    # Get all rooms that the user is a part of
    rooms = Room.objects.filter(users=request.user)
    return render(request, "rooms/room_list.html", {"rooms": rooms})