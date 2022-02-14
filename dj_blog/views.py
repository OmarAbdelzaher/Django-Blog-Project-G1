from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import *
from django.contrib import messages
import os
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required

def registerpage(request):
    # handling the checking for already logged in later
    user_form = RegistrationForm()
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')
    context = {'user_form': user_form}
    return render(request, 'dj_blog/register.html', context)

# validation to the login page (check user already logged in if not -> authenticate the username and password )


@csrf_exempt
def loginpage(request):
    # handling the checking for already logged in later
    login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(data=request.POST)
        if(login_form.is_valid()):
            username = request.POST['username']
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                # handling the checking for blocked users here later
                login(request, user)
                if request.GET.get('next') is not None:
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('landing')
    context = {"login_form": login_form}
    return render(request, 'dj_blog/login.html', context)

# Home Page
def landing(request):
    categories = Category.objects.all()
    posts = Post.objects.order_by('-date_of_publish')
    
    names = []
    for post in posts:
        names.append(User.objects.get(id=post.user_id))
        
    imgs = Post.objects.values_list('picture', flat=True)
    imageBases = []

    for i in range(len(imgs)):
        imageBases.append(os.path.basename(imgs[i]))

    my_list = zip(posts, imageBases, names)

    context = {'mylist': my_list,'categories': categories}
    return render(request, 'dj_blog/landing.html', context)

# def post(request):
#     return render(request, 'dj_blog/post.html')


# def postPage(request):
#     posts = Post.objects.order_by('-date_of_publish')
    
#     names = []
#     for post in posts:
#         names.append(User.objects.get(id=post.user_id))
        
    
#     imgs = Post.objects.values_list('picture', flat=True)
#     imageBases = []

#     for i in range(len(imgs)):
#         imageBases.append(os.path.basename(imgs[i]))

#     my_list = zip(posts, imageBases,names)

#     context = {'mylist': my_list}
#     return render(request, 'dj_blog/posts-page.html', context)


def logoutpage(request):
    auth.logout(request)
    return redirect('landing')


def manageBlog(request):
    return render(request, 'dj_blog/manageblog.html')


# catagories subscribe
def subscribe(request, cat_id):
    user = request.user
    category = Category.objects.get(id=cat_id)
    category.user.add(user)
    return redirect("landing")

# catagories unsubscribe
def unsubscribe(request, cat_id):
    user = request.user
    category = Category.objects.get(id=cat_id)
    category.user.remove(user)
    return redirect("landing")

def addPost(request):
    post_form = PostForm()
    tag_form = TagsForm()
    
    if request.method == 'POST':
        post_form = PostForm(request.POST,request.FILES)
        tag_form = TagsForm(request.POST)
        if post_form.is_valid() and tag_form.is_valid():
            obj = post_form.save(commit=False)
            obj.user = request.user
            obj.save()
            
            tag_obj = tag_form.save(commit=False)
            splitted_tags = str(tag_obj).split(',')
            for tag in splitted_tags:
                newTag = PostTags.objects.create(tag_name = tag)
                newTag.save()
                obj.tag.add(newTag)
                
            obj.save()
            return redirect('landing')

    context = {'post':post_form,'tag':tag_form}
    return render(request,'dj_blog/add-post.html',context)

def catPosts(request,CatId):
    cat_post = Post.objects.filter(category_id = CatId).order_by('-date_of_publish')
    
    names = []
    for post in cat_post:
        names.append(User.objects.get(id=post.user_id))
    
    imgs = []
    for post in cat_post:
        imgs.append(str(post.picture))
    
    imageBases = []
    for i in range(len(imgs)):
        imageBases.append(os.path.basename(imgs[i]))
    
    my_list = zip(cat_post, imageBases, names)

    context = {'mylist': my_list}
    return render(request, 'dj_blog/cat-posts.html',context)

# the user must be logged in to interact with the posts
@login_required(login_url='login')
def AddLike(request,post_id):
    # get the post that the user interacted with
    post = Post.objects.get(id=post_id)
    img = str(post.picture)
    print(img)
    base_name = os.path.basename(img)
    print(base_name)    
    # check if there is a dislike
    is_dislike = False
    for dislike in post.dislikes.all():
        if dislike == request.user:
            is_dislike = True
            break
        
    # if the user clicked on the like button, remove the dislike
    if is_dislike:
        post.dislikes.remove(request.user)
    
    # check if there is a like
    is_like = False
    for like in post.likes.all():
        if like == request.user:
            is_like = True
            break
        
    # if the user clicked on the like button, add the like
    if not is_like:
        post.likes.add(request.user)
    
    # if the user clicked on the like button (already liked), remove the like
    if is_like:
        post.likes.remove(request.user)

    context = {'post':post,'image':base_name}
    return render(request, 'dj_blog/post.html',context)

# the user must be logged in to interact with the posts
@login_required(login_url='login')
def AddDislike(request,post_id):
    # get the post that the user interacted with
    post = Post.objects.get(id=post_id)
    
    # check if there is a like
    is_like = False
    for like in post.likes.all():
        if like == request.user:
            is_like = True
            break
        
    # if the user clicked on the dislike button, remove the like
    if is_like:
        post.likes.remove(request.user)
    
    # check if there is a dislike
    is_dislike = False
    for dislike in post.dislikes.all():
        if dislike == request.user:
            is_dislike = True
            break
    
    # if the user clicked on the dislike button, add the dislike
    if not is_dislike:
        post.dislikes.add(request.user)
    
    # if the user clicked on the dislike button (already disliked), remove the dislike
    if is_dislike:
        post.dislikes.remove(request.user)
    
    context = {'post':post}
    return render(request, 'dj_blog/post.html',context)