from unicodedata import category
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from dj_blog.models import Account,Category
from dj_blog.forms import CategoryForm
# Create your views here.

def starter(request):
    users = User.objects.filter(is_staff= False) 
    context={'users':users}
    return render(request,'dj_admin/starter.html',context)

def promoteUser(request,id):
    user=User.objects.get(id = id)
    if not islocked(user):
        user.is_staff=True
        user.is_superuser=True
        user.save()
        return redirect('starter')
    else : 
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

# add category 
def addCategory(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("category")
    context = {"cat_form": form}
    return render(request, "dj_admin/categoryform.html", context)

# delete category 
def deleteCategory(request,cat_id):
    category= Category.objects.get(id=cat_id)
    category.delete()
    return redirect("category")


def editCategory(request,cat_id):
    category = Category.objects.get(id= cat_id)
    # put the category object which we want to edit into the form method by assigning it to the instance attribute 
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            return redirect('category')
    context = {"cat_form":form}
    return render (request,"dj_admin/editcategory.html",context)