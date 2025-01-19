from django.shortcuts import render
from .models import Salon, Message
from .forms import SalonForm


def list_all_salons(request):
    salons = Salon.objects.all()  # Fetch all salons
    return render(request, 'salons/list_all.html', {'salons': salons})


def salon_view(request):
    return render(request, 'salon.html')


def list_salons(request):
    salons = request.user.salons.all()
    return render(request, 'salons/list.html', {'salons': salons})


def create_salon(request):
    if request.method == 'POST':
        form = SalonForm(request.POST)
        if form.is_valid():
            salon = form.save(commit=False)
            salon.created_by = request.user
            salon.save()
            salon.members.add(request.user)  # Add creator as a member
            return redirect('salons:list')
    else:
        form = SalonForm()
    return render(request, 'salons/create.html', {'form': form})



def salon_detail(request, id):
    salon = get_object_or_404(Salon, id=id)
    if request.user not in salon.members.all():
        raise PermissionDenied
    messages = salon.messages.all().order_by('-created_at')
    return render(request, 'salons/detail.html', {'salon': salon, 'messages': messages})


SALON_DETAIL_URL = 'salons:detail'

def invite_to_salon(request, id):
    salon = get_object_or_404(Salon, id=id)
    if request.user not in salon.members.all():
        raise PermissionDenied
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            salon.members.add(user)
            return redirect(SALON_DETAIL_URL, id=salon.id)
    else:
        form = InviteForm()
    return render(request, 'salons/invite.html', {'form': form, 'salon': salon})



def delete_salon(request, id):
    salon = get_object_or_404(Salon, id=id, created_by=request.user)
    salon.delete()
    return redirect('salons:list')


def list_messages(request, id):
    salon = get_object_or_404(Salon, id=id)
    if request.user not in salon.members.all():
        raise PermissionDenied
    messages = salon.messages.all().order_by('-created_at')
    return JsonResponse({'messages': list(messages.values())})


def send_message(request, id):
    salon = get_object_or_404(Salon, id=id)
    if request.user not in salon.members.all():
        raise PermissionDenied
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.salon = salon
            message.user = request.user
            message.save()
            return redirect('salons:detail', id=salon.id)
    else:
        form = MessageForm()
    return render(request, 'messages/send.html', {'form': form, 'salon': salon})


def delete_message(request, id):
    message = get_object_or_404(Message, id=id, user=request.user)
    message.delete()
    return redirect('salons:detail', id=message.salon.id)



def leave_salon(request, id):
    salon = get_object_or_404(Salon, id=id)
    salon.members.remove(request.user)
    return redirect('salons:list')
