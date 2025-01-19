from django import forms
from .models import Salon

class SalonForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = ['name']  # Include only the name field for salon creation
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter salon name',
            }),
        }
        labels = {
            'name': 'Salon Name',
        }


