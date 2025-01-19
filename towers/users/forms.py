from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class SignupForm(forms.ModelForm):
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ['nom', 'prenom', 'email', 'password', 'photo']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")
        return password_confirmation


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password
    
    
class ModifyUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nom', 'prenom', 'email', 'photo']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")
        return password_confirmation