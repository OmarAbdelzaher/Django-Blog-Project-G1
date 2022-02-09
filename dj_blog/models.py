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



class Comment(models.Model):
    comment_body=models.CharField(max_length=100)
    comment_time=models.DateField(null=True)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    post_id=models.ForeignKey(Post,on_delete=models.CASCADE)     
    
 
#  Reply Table   
class Reply(models.Model):
    reply_body=models.CharField(max_length=100)
    reply_time=models.TimeField(null=True)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    comment_id=models.ForeignKey(Comment, on_delete=models.CASCADE)    