from django import forms
from .models import Room
from django.contrib.auth import get_user_model

User = get_user_model()

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name"]

class InviteUserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User to Invite")
