from django.contrib import admin

# Register your models here.
from .models import Salon 
from .models import Message

admin.site.register(Salon)
admin.site.register(Message)

