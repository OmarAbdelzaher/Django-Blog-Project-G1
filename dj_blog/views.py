from django.shortcuts import render
from .models import *
# Create your views here.

def post(request):
    return render(request, 'dj_blog/post.html')

def postPage(request):
    posts = Post.objects.all()
    print(posts)
    context = {'posts':posts}
    return render(request,'dj_blog/posts-page.html',context)