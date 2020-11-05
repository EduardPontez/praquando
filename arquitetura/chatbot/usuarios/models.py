from django.db import models

# Create your models here.
class Usuario(models.Model):
    
    code = models.CharField(max_Length = 15)
    #Código do usuário será o próprio Code

    active = models.IntegerField()
    name = models.CharField(max_Length = 100)
    email = models.CharField(max_Length = 100)
    email = models.CharField(max_Length = 100)
    user = models.CharField(max_Length = 50)
    password = models.CharField(max_Length = 10)
    
    def __str__(self):
        return self.name