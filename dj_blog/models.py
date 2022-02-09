from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    user_type = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    avatar = models.ImageField(null=True)
    # def save(self,*args,**kwargs):
    #     self.set_password(self.password)
    #     super().save(*args,**kwargs)
    
    