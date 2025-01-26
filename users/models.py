from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
