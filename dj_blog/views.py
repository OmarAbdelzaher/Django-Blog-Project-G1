from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import *
from django.contrib import messages
import os
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from dj_admin.views import islocked
# import email confirmation stuff
from django.core.mail import send_mail
from django.conf import settings

# import pagination stuff
from django.core.paginator import Paginator

# from django.utils.functional import SimpleLazyObject




def registerpage(request):
    # handling the checking for already logged in later
    user_form = RegistrationForm()
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            account = Account.objects.create(user=user)
            account.is_locked = False 
            account.save()
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
                # handling the checking for blocked users 
                if (user.is_staff) : # to check first if the user is admin or not 
                     login(request, user)
                     if request.GET.get('next') is not None:
                        return redirect(request.GET.get('next'))
                     else:
                        return redirect('landing')
                elif islocked(user): # to check if the user is blocked or not 
                    messages.info(request,"This Account is blocked , Please contact the admin")
                else :
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
    
    #set up pagination
    num_of_posts=5
    p= Paginator(Post.objects.order_by('-date_of_publish'), num_of_posts)
    page= request.GET.get('page')
    pagination_posts=p.get_page(page)

    # End of setting pagination

    nums= "a" * pagination_posts.paginator.num_pages
    pg=pagination_posts

    context = {'posts': posts,'categories': categories,'pg':pg ,'nums':nums}
    return render(request, 'dj_blog/landing.html', context)

def PostPage(request,post_id):
    post = Post.objects.get(id=post_id)
    context = {'post':post}
    return render(request, 'dj_blog/post.html',context)

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
    try:
        send_mail("subscribed to a new category",
                'hello ,'+user.first_name+" "+user.last_name+'\nyou have just subscribed to category '+category.cat_name,
                'settings.EMAIL_HOST_USER', [user.email], fail_silently=False,)
    except Exception as ex:
        log("couldn't send email message"+str(ex))
        
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

# Edit Post
def updatePost(request,post_id):

    post=Post.objects.get(id=post_id)
    form=PostForm(instance=post)
    tag_form = TagsForm()
    # tags=PostTags.objects.get(tag_name=post.tag)
    # tags= TagsForm(instance=frmtag)

    if request.method == 'POST':
        post = PostForm(request.POST,request.FILES,instance=post)
        # tag_form = TagsForm(request.POST)
        if post.is_valid():
            obj = post.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('landing')


    context={'form':form}

    return render(request,'dj_blog/updatePost.html',context)

# Delete post
def DeletePost(request,post_id):
    post=Post.objects.get(id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect ('landing')


    context={'post':post}

    return render(request,'dj_blog/delete-post.html',context)


def catPosts(request,CatId):
    cat_post = Post.objects.filter(category_id = CatId).order_by('-date_of_publish')
    context = {'cat_post': cat_post}
    return render(request, 'dj_blog/cat-posts.html',context)

# the user must be logged in to interact with the posts
@login_required(login_url='login')
def AddLike(request,post_id):
    # get the post that the user interacted with
    post = Post.objects.get(id=post_id)
    img = str(post.picture)
    base_name = os.path.basename(img)

    # check if there is a dislike
    is_dislike = False
    for dislike in post.dislikes.all():
        print(dislike)
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

    post.save()
    return redirect('post',post_id)

# the user must be logged in to interact with the posts
@login_required(login_url='login')
def AddDislike(request,post_id):
    # get the post that the user interacted with
    post = Post.objects.get(id=post_id)
    
    # check if there is a like
    is_like = False
    for like in post.likes.all():
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
    
    post.save()
    
    return redirect('post',post_id)


@login_required(login_url='login')
def add_comment(request, post_id):
    post = get_object_or_404(Post,id=post_id)
    if request.method == 'POST':
        user = request.user
        print(user)
        comment_text = request.POST.get('text')
        Comment(user=user , post_id=post, comment_body=comment_text).save() 
    else:
        return redirect('post', post_id)
    return redirect('post', post_id)


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(title=searched)
        tags = Post.objects.filter(tag__tag_name=searched)
        tag = PostTags.objects.filter(tag_name=searched)

        context = {'searched':searched, 'posts':posts, 'tags':tags, 'tag':tag}
        
        return render(request, 'dj_blog/search.html',context)
    else:
        return render(request, 'dj_blog/search.html',{})
