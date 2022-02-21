from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from dj_admin.forms import LoginAdmin
from dj_blog.models import *
from dj_blog.forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from .forms import LoginAdmin

# Create your views here.
# function to allow the admins to login in admin panel
def loginAdmin(request):
    login_form = LoginAdmin()
    if request.method == "POST":
            login_form = LoginAdmin(data=request.POST)
            # checking if the login form is valid or not 
            if(login_form.is_valid()):
                # get the data for username and password from the post request then checking if they exists in the database  
                username = request.POST['username']
                password = request.POST["password"]
                user = authenticate(username=username, password=password)
                if user is not None :
                    if user.is_staff :
                        login(request,user)
                        if request.GET.get('next') is not None:
                            return redirect(request.GET.get('next'))
                        else:
                            return redirect('starter')
                    else : 
                        messages.info(request,"This Page is only for admins ")
    context = {"login_form": login_form}
    return render(request, 'dj_admin/loginadmin.html', context)

#function to allow the admins to logout from the panel 
def logoutAdmin(request):
    logout(request)
    return redirect("admin")

# this is the starter page for the admin page

@staff_member_required(login_url="admin")
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
@staff_member_required(login_url="admin")
def showAdmins(request):
    admins=User.objects.filter(is_staff = True , is_superuser=True)
    context={'admins':admins}
    return render(request,'dj_admin/admins.html',context)

# lock the required account first then lock the user associated to that account
def lock_user(user):
        account = Account.objects.get(user=user)
        account.is_locked = True
        account.save()

@staff_member_required(login_url="admin")
def lockUser(request,id):
    user = User.objects.get(id=id)
    lock_user(user)
    return redirect('starter')

# unlock the required account first then unlock the user associated to that account 
def unlock_user(user):
        account = Account.objects.get(user=user)
        account.is_locked = False
        account.save()

@staff_member_required(login_url="admin")
def unlockUser(request,id):
    user = User.objects.get(id=id)
    unlock_user(user)
    return redirect('starter')

# function to return the status of the account if it is locked or not 
def islocked(user):
    return user.account.is_locked

# view to show the catagories 
@staff_member_required(login_url="admin")
def showCategory(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request,'dj_admin/categories.html',context)

# add category 
@staff_member_required(login_url="admin")
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
@staff_member_required(login_url="admin")
def deleteCategory(request,cat_id):
    category= Category.objects.get(id=cat_id)
    category.delete()
    return redirect("category")

@staff_member_required(login_url="admin")
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


@staff_member_required(login_url="admin")
def showPosts(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request,'dj_admin/posts.html',context)

@staff_member_required(login_url="admin")
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


#view to edit specific forbidden word using the word id
@staff_member_required(login_url="admin") 
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
            # get the editted tags
            tags = post_form.cleaned_data['tag']
            
            for tag in tags:
                newTag = PostTags.objects.get(tag_name = tag)
                #add the tags to related post
                obj.tag.add(newTag)
                obj.save()
            
            tag_obj = request.POST.get('tag_name')
            splitted_tags = str(tag_obj).split(',')
            
            all_tags = PostTags.objects.all()
            is_exist = False
            
            # check if the splitted is empty to validate the input of user
            if splitted_tags[0] != '':
                for tag in splitted_tags:
                    for compare in all_tags:
                        print(tag,compare)
                        if str(tag) == str(compare):    
                            is_exist = True
                            
                    if not is_exist:
                        newTag = PostTags.objects.create(tag_name = tag)
                    newTag.save()
                    obj.tag.add(newTag)
                    is_exist = False
            obj.save()
            return redirect('post')
 
    return render (request,"dj_admin/editpost.html",context)

@staff_member_required(login_url="admin")
def deletePost(request,post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect("post")

# view to add the forbidden words in admin page 
@staff_member_required(login_url="admin")
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
@staff_member_required(login_url="admin")
def showForbidden(request):
    forbidden_words = ForbiddenWords.objects.all()
    context = {'forbidden_words' : forbidden_words}
    return render(request, "dj_admin/forbiddenwords.html", context)

# view to delete specific forbidden word using the word id
@staff_member_required(login_url="admin")
def delForbidden(request,word_id):
    forbidden_words = ForbiddenWords.objects.get(id = word_id)
    forbidden_words.delete()
    return redirect('forbiddenwords')

#view to edit specific forbidden word using the word id 
@staff_member_required(login_url="admin")
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
