from django.db import models
from users.models import User  


class Salon(models.Model):
    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=255)  
    created_by = models.ForeignKey(User, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)  
    members = models.ManyToManyField(User, related_name='salons', blank=True)  

    def __str__(self):
        return self.name



class Message(models.Model):
    id = models.AutoField(primary_key=True)  
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='messages')  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    text = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user.username}: {self.text[:30]}"  
