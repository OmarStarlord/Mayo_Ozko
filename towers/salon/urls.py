from django.urls import path
from . import views

urlpatterns = [ 
    path('salon/', views.salon_view, name='salon'),
    path('list_all_salons/', views.list_all_salons, name='list_all'),
]
