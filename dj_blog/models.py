from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Account model extends from User (built-in-Model) and add some extra fields
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    TYPE_CHOICES = (('user','User'),('admin','Admin'))
    user_type = models.CharField(max_length=50,choices=TYPE_CHOICES)
    avatar = models.ImageField(null=True,upload_to = 'dj_blog/static/img/Users Images/')
    
    def __str__(self):  
        return self.username

class Category(models.Model):
    cat_name=models.CharField(max_length=100)

    def __str__(self):
        return self.cat_name

class Post(models.Model):
    title=models.CharField(max_length=50,null=True)
    picture=models.ImageField(null=True)
    content=models.CharField(max_length=255)
    likes=models.IntegerField(null=True)
    dislikes=models.IntegerField(null=True)
    date_of_publish=models.DateField(null=True)
    user_id =models.ForeignKey(User,on_delete=models.CASCADE)
    cat_id=models.ForeignKey(Category,on_delete=models.CASCADE)

    # return post title
    
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

class PostTags(models.Model):
    tag=models.CharField(max_length=100)
    post_id=models.ForeignKey(Post,on_delete=models.CASCADE) 

class UserCategory(models.Model):
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    cat_id=models.ForeignKey(Category, on_delete=models.CASCADE)

