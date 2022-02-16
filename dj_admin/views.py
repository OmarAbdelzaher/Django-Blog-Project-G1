from unicodedata import category
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from dj_blog.models import *
from dj_blog.forms import *
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

def showPosts(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request,'dj_admin/posts.html',context)

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
            return redirect('post')

    context = {'post_form':post_form,'tag_form':tag_form}
    return render(request,'dj_admin/postform.html',context)


def editPost(request,post_id):
    post = Post.objects.get(id= post_id)
    post_form = PostForm(instance=post)
    # tagInstance = []
    for tag in post.tag.all():
        print(tag)
        newTag = PostTags.objects.get(tag_name=tag)
        tag_form = TagsForm(instance=newTag)
        # tagInstance.append(newTag)
 
    # print(tagInstance)
    
    
    # if request.method == 'POST':
    #     form = PostForm(request.POST,instance=post)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('post')
    context = {"post_form":post_form,'tag_form':tag_form}
    return render (request,"dj_admin/editpost.html",context)

def deletePost(request,post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect("post")