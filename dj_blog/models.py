from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Account model extends from User (built-in-Model) and add some extra fields
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='images/default.png',upload_to = 'Avatars/')
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Category Model
class Category(models.Model):
    cat_name=models.CharField(max_length=100)
    user = models.ManyToManyField(User,related_name='categories')

    def __str__(self):
        return self.cat_name

# Tags Model
class PostTags(models.Model):
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return self.tag_name

# Post Model    
class Post(models.Model):
    title = models.CharField(max_length=50)
    picture = models.ImageField(null=True,upload_to='images/')
    content = models.CharField(max_length=255)
    likes = models.ManyToManyField(User,blank=True,related_name='likes')
    dislikes = models.ManyToManyField(User,blank=True,related_name='dislikes')
    date_of_publish = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    tag = models.ManyToManyField(PostTags,blank=True)
      
    def __str__(self):
        return self.title

# Comment Model    
class Comment(models.Model):
    comment_body=models.CharField(max_length=100)
    comment_time=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post_id=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments") 
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+') #Parent to hold comment id

    def __str__(self):
        return self.user.username
    
# Reply Model  
class Reply(models.Model):
    reply_body=models.CharField(max_length=100)
    reply_time=models.TimeField(null=True)
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    comment_id=models.ForeignKey(Comment, on_delete=models.CASCADE)


class ForbiddenWords(models.Model):
    forbidden_word=models.CharField(max_length=100)

    def __str__(self):
        return self.forbidden_word    




