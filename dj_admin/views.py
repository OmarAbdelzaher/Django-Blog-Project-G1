from ast import For
from unicodedata import category
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from dj_blog.models import *
from dj_blog.forms import *

# Create your views here.

# this is the starter page for the admin page 
def starter(request):
    # get all normal users 
    users = User.objects.filter(is_staff= False) 
    context={'users':users}
    return render(request,'dj_admin/starter.html',context)

# view to promote the user to an admin 
def promoteUser(request,id):
    user=User.objects.get(id = id)
    #check if the user is not blocked he can be promoted .. and that's by making the is_staff attribute and is_superuser equal true 
    if not islocked(user):
        user.is_staff=True
        user.is_superuser=True
        user.save()
        return redirect('starter')
    else : 
        return redirect('starter')

# view to show the all the admins 
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

# function to return the status of the account if it is locked or not 
def islocked(user):
    return user.account.is_locked

# view to show the catagories 
def showCategory(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request,'dj_admin/categories.html',context)

# add category 
def addCategory(request):
    # create catageory form 
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # checking the form if it's valid or not 
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


# show all posts to admin
def showPosts(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request,'dj_admin/posts.html',context)

# adding post as a user
def addPost(request):
    # get the forms empty to be filled
    post_form = PostForm()
    tag_form = TagsForm()
    
    # if the add button pressed save the input data after validation
    if request.method == 'POST':
        post_form = PostForm(request.POST,request.FILES)
        tag_form = TagsForm(request.POST)
        if post_form.is_valid() and tag_form.is_valid():
            obj = post_form.save(commit=False)
            obj.user = request.user
            obj.save()
            
            # get object from tag before saving it
            tag_obj = tag_form.save(commit=False)
            # split the separated tags by comma
            splitted_tags = str(tag_obj).split(',')
            # loop on each tag splitted, add to the related post and save it
            for tag in splitted_tags:
                newTag = PostTags.objects.create(tag_name = tag)
                newTag.save()
                obj.tag.add(newTag)
                
            obj.save()
            return redirect('post')

    context = {'post_form':post_form,'tag_form':tag_form}
    return render(request,'dj_admin/postform.html',context)

# edit post by admin
def editPost(request,post_id):
    # get the post with its saved data
    post = Post.objects.get(id= post_id)
    tags = post.tag.all()
    post_form = PostForm(instance=post)
    # get empty form for new tags
    tag_form = TagsForm()
    
    context = {}
    context['post_form'] = post_form
    context['tag_form'] = tag_form
    
    if request.method == 'POST':
        # get the new editted data
        post_form = PostForm(request.POST,request.FILES,instance=post)
        tag_form = TagsForm(request.POST)
        if post_form.is_valid():
            obj = post_form.save(commit = False)
            obj.user = request.user
            # remove the old tags to be replaced with the new editted tags
            obj.tag.clear()
            obj.save()
            # get the ediited tags
            tags = post_form.cleaned_data['tag']
            
            for tag in tags:
                newTag = PostTags.objects.get(tag_name = tag)
                #add the tags to related post
                obj.tag.add(newTag)
                obj.save()
            
            tag_obj = request.POST.get('tag_name')
            splitted_tags = str(tag_obj).split(',')
            
            # check if the spliited is empty to validate the input of user
            if splitted_tags[0] != '':
                for tag in splitted_tags:
                    newTag = PostTags.objects.create(tag_name = tag)
                    newTag.save()
                    obj.tag.add(newTag)
            obj.save()
            return redirect('post')
 
    return render (request,"dj_admin/editpost.html",context)

# delete post by admin
def deletePost(request,post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect("post")

# view to add the forbidden words in admin page 
def addForbidden(request):
    form = ForbiddenWordsForm()
    if request.method == 'POST':
        form = ForbiddenWordsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("forbiddenwords")
    context = {"word_form": form}
    return render(request, "dj_admin/forbiddenwordform.html", context)


# view to show all the forbidden words 
def showForbidden(request):
    forbidden_words = ForbiddenWords.objects.all()
    context = {'forbidden_words' : forbidden_words}
    return render(request, "dj_admin/forbiddenwords.html", context)

# view to delete specific forbidden word using the word id
def delForbidden(request,word_id):
    forbidden_words = ForbiddenWords.objects.get(id = word_id)
    forbidden_words.delete()
    return redirect('forbiddenwords')

#view to edit specific forbidden word using the word id 
def editForbidden(request,word_id):
    forbidden_words = ForbiddenWords.objects.get(id= word_id)
    form = ForbiddenWordsForm(instance=forbidden_words)
    if request.method == 'POST':
        form = ForbiddenWordsForm(request.POST,instance=forbidden_words)
        if form.is_valid():
            form.save()
            return redirect('forbiddenwords')
    context = {"word_form":form}
    return render (request,"dj_admin/editforbiddenwords.html",context)
