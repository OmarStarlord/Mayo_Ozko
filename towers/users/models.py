from django.db import models

# Create your models here.
class User(models.Model):
    # id needs to be incremented automatically
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='profile_pics', default='default.jpg')
    def __str__(self):
        return self.nom + ' ' + self.prenom
    
    
    