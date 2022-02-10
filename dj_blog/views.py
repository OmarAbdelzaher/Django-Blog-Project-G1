from django.shortcuts import render
from .models import *
import os
# Create your views here.

def post(request):
    return render(request, 'dj_blog/post.html')

def postPage(request):
    posts = Post.objects.all()
    imgs = Post.objects.values_list('picture', flat=True)
    
    imageBases = []
    
    for i in range(len(imgs)):
        imageBases.append(os.path.basename(imgs[i]))
    
    my_list = zip(posts,imageBases)
    
    # print(imageBases)
    # dict = {'posts':posts,'images':imageBases}
    context = {'mylist':my_list}
    return render(request,'dj_blog/posts-page.html',context)
