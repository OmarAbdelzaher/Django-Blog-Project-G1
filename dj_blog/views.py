from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,authenticate
from .forms import *
from .models import *

#Create your views here.

# validation to the registration form 
def registerpage(request):
    # handling the checking for already logged in later 
    user_form=RegistrationForm()
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')
    context={'user_form':user_form}
    return render(request, 'dj_blog/register.html', context)

# validation to the login page (check user already logged in if not -> authenticate the username and password )
def loginpage(request):
    # handling the checking for already logged in later 
    login_form=LoginForm()
    if request.method == "POST":
            login_form = LoginForm(data=request.POST)
            if(login_form.is_valid()):
                username = request.POST['username']
                password = request.POST["password"]
                user = authenticate(username=username, password=password)
                if user is not None:  
                    # handling the checking for blocked users here later 
                    login(request,user)
                    if request.GET.get('next') is not None:
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect('home')
    context = {"login_form": login_form}
    return render(request, 'dj_blog/login.html', context)


#Experimental Page 
def home (request):
    return HttpResponse ('<h1>Welcome Home Page </h1>')


def post(request):
    return render(request, 'dj_blog/post.html')

def postPage(request):
    posts = Post.objects.all()
    print(posts)
    context = {'posts':posts}
    return render(request,'dj_blog/posts-page.html',context)