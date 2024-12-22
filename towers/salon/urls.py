from django.urls import path
from . import views

urlpatterns = [
     #empty 
    path('salon/', views.salon_view, name='salon'),
    # Add more salon-related URLs here
]
