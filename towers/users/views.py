from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignupForm
from .models import User
from .forms import LoginForm



# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)  
            user.set_password(form.cleaned_data['password']) 
            user.is_active = True  
            user.is_staff = False  
            user.save()  
            return redirect('login')  
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})



#login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            
            user = authenticate(request, username=email, password=password)  
            if user is not None:
                print("success")
                login(request, user)  
                return redirect('success')  

            else:
                form.add_error(None, 'Invalid email or password')
        else:
            print("Form is not valid") 
            
    else:
        form = LoginForm()

    
    return render(request, 'login.html', {'form': form})


def success_view(request):
    return render(request, 'success.html')