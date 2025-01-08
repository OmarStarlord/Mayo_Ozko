from django.contrib import admin
from .models import Salon, Message
from users.models import User  

class SalonAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at') 
    search_fields = ('name',)  
    filter_horizontal = ('members',)  
    autocomplete_fields = ['created_by'] 


# Register the models
admin.site.register(Salon, SalonAdmin)  
admin.site.register(Message) 