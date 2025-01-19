from django.urls import path
from . import views

app_name = 'salons'  # Namespace for your app

urlpatterns = [
    # General salon views
    path('', views.list_salons, name='list'),  # List user's salons
    path('list_all/', views.list_all_salons, name='list_all'),  # List all salons (admin or general view)
    path('create/', views.create_salon, name='create'),  # Create a new salon
    path('<int:id>/', views.salon_detail, name='detail'),  # Salon detail view
    path('<int:id>/invite/', views.invite_to_salon, name='invite'),  # Invite users to a salon
    path('<int:id>/delete/', views.delete_salon, name='delete'),  # Delete a salon
    path('<int:id>/leave/', views.leave_salon, name='leave'),  # Leave a salon

    # Message-related views
    path('<int:id>/messages/', views.list_messages, name='list_messages'),  # List messages in a salon
    path('<int:id>/messages/send/', views.send_message, name='send_message'),  # Send a message
    path('messages/<int:id>/delete/', views.delete_message, name='delete_message'),  # Delete a message
]
