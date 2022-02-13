from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import *
from django.contrib import messages
import os
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import auth

# validation to the registration form


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


# Experimental Page
def home(request):
    return HttpResponse('<h1>Welcome Home Page </h1>')

# Home Page


def landing(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'dj_blog/landing.html', context)


def post(request):
    return render(request, 'dj_blog/post.html')


def postPage(request):
    posts = Post.objects.all()
    imgs = Post.objects.values_list('picture', flat=True)

    imageBases = []

    for i in range(len(imgs)):
        imageBases.append(os.path.basename(imgs[i]))

    my_list = zip(posts, imageBases)

    context = {'mylist': my_list}
    return render(request, 'dj_blog/posts-page.html', context)


def logoutpage(request):
    auth.logout(request)
    return redirect('landing')


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
