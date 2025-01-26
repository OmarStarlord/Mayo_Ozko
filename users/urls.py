from django.urls import path
from .views import CustomLoginView, LogoutView, signup, edit_profile

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    path('edit-profile/', edit_profile, name='edit_profile'),
]
