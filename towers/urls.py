"""towers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from users.views import CustomLoginView

urlpatterns = [
    # Admin Panel URL
    path('admin/', admin.site.urls),
    # i want the index to take me to the users login page
    path('', CustomLoginView.as_view(), name='login'),
    # Include URLs from the 'users' app
    path('users/', include('users.urls')),  
    
    # Include URLs from the 'rooms' app
    path('rooms/', include('rooms.urls')),  
    
    
]
