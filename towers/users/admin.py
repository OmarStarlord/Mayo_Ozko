from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'is_active', 'is_staff')
    search_fields = ('email', 'nom', 'prenom')

admin.site.register(User, UserAdmin)
