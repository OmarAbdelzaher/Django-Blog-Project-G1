from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from dj_blog.models import Account,Category
# Create your views here.

def starter(request):
    users = User.objects.filter(is_staff= False) 
    context={'users':users}
    return render(request,'dj_admin/starter.html',context)

def promoteUser(request,id):
    user=User.objects.get(id = id)
    user.is_staff=True
    user.is_superuser=True
    user.save()
    return redirect('starter')

def showAdmins(request):
    admins=User.objects.filter(is_staff = True , is_superuser=True)
    context={'admins':admins}
    return render(request,'dj_admin/admins.html',context)

# lock the required account first then lock the user associated to that account
def lock_user(user):
        account = Account.objects.get(user=user)
        account.is_locked = True
        account.save()
    
def lockUser(request,id):
    user = User.objects.get(id=id)
    lock_user(user)
    return redirect('starter')

# unlock the required account first then unlock the user associated to that account 
def unlock_user(user):
        account = Account.objects.get(user=user)
        account.is_locked = False
        account.save()
    
def unlockUser(request,id):
    user = User.objects.get(id=id)
    unlock_user(user)
    return redirect('starter')

def islocked(user):
    return user.account.is_locked

def showCategory(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request,'dj_admin/categories.html',context)

