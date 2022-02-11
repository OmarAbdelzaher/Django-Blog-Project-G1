from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,authenticate
from .forms import CreateUserForm
from django.contrib import messages
from .models import *

#Create your views here.

# validation to the registration form 
def registerpage(request):
    # is_authenticaed with http request checks whether the user is already logged in or not 
    if request.user.is_authenticated:
        return redirect('home')
    else :
        register_form = CreateUserForm()
        if request.method=='POST':
            register_form = CreateUserForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                msg = 'User account created for username: ' + register_form.cleaned_data.get('username')
                messages.info(request, msg)
                return redirect('home')
        context = {'register_form': register_form}
        return render(request, 'dj_blog/register.html', context)


# validation to the login form 
def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else :
        if request.method == 'POST':
            name = request.POST.get('username')
            passwd = request.POST.get('password')
            user = authenticate(request,username= name, password =passwd)
            if user is not None:
                login(request, user)
                # next here specifies whether the user will redirect to the page he came from or not 
                if request.GET.get('next') is not None:
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('home')
                
            else:
                messages.warning(request, 'User name or password is incorrect')
        return render(request, 'dj_blog/login.html')

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