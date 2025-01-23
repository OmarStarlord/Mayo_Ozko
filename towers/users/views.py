from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View

from .models import User 
from django.shortcuts import render


User = get_user_model()

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "profile_pic"]

class CustomLoginView(LoginView):
    template_name = 'login.html'  
    
    def get_success_url(self):
        return reverse_lazy('room_list')




class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "profile_pic", "first_name", "last_name"]

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # After saving, log the user in and redirect to the room list
            user = form.cleaned_data.get('username')
            user = User.objects.get(username=user)
            
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

# Edit Profile View
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')  # Redirect to the profile page after saving
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'  
    
    def get_success_url(self):
        return reverse_lazy('room_list')  # Redirect to room_list after successful login


# Call logout function
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")
