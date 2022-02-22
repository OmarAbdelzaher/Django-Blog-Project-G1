from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import *
from .models import *
from django.contrib import messages
import os
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from dj_admin.views import islocked

# import email confirmation stuff
from django.core.mail import send_mail
from django.conf import settings

# import pagination stuff
from django.core.paginator import Paginator




# resgistration page 
def registerpage(request):
    # checking if the user is already logged or not 
    if not request.user.is_authenticated :
        # creating resgistration form 
        user_form = RegistrationForm()

        if request.method == "POST":
            user_form = RegistrationForm(request.POST)
            if user_form.is_valid():
                # if the form is valid , save the form then create an account for the user and initialize account is locked equal false         
                user = user_form.save()
                account = Account.objects.create(user=user)
                account.is_locked = False 
                account.save()
                return redirect('login')
        context = {'user_form': user_form}
        return render(request, 'dj_blog/register.html', context)

    else :
        return redirect("landing")

# validation to the login page (check user already logged in if not -> authenticate the username and password )

@csrf_exempt
def loginpage(request):
    # checking if the user is already logged or not  
    if not request.user.is_authenticated :

        login_form = LoginForm()
        if request.method == "POST":
            login_form = LoginForm(data=request.POST)
            # checking if the login form is valid or not 
            
            if(login_form.is_valid()):
                # get the data for username and password from the post request then checking if they exists in the database  
                username = request.POST['username']
                password = request.POST["password"]
                user = authenticate(username=username, password=password)

                if user is not None:
                    if (user.is_staff) : # to check first if the user is admin or not 
                        login(request, user)
                        # checking if the next object is have a specific url or not if have we will redirect it 
                        if request.GET.get('next') is not None:
                            return redirect(request.GET.get('next'))
                        else:
                            return redirect('landing')
                    elif islocked(user): # to check if the user is blocked or not 
                        messages.info(request,"This Account is blocked , Please contact the admin at djblog2022@gmail.com")
                    else :
                        # this else if the user isn't an admin or a blocked user 
                        login(request, user)
                        if request.GET.get('next') is not None:
                            return redirect(request.GET.get('next'))
                        else:
                            return redirect('landing')

        context = {"login_form": login_form}
        return render(request, 'dj_blog/login.html', context)
    else :
        return redirect("landing")

# Home Page
def landing(request):
    categories = Category.objects.all()
    posts = Post.objects.order_by('-date_of_publish')
    tags=PostTags.objects.all()
    
    #set up pagination
    # number posts in one page
    num_of_posts=5
    p= Paginator(Post.objects.order_by('-date_of_publish'), num_of_posts)
    page= request.GET.get('page')
    pagination_posts=p.get_page(page)

    # To show number of pages (1,2,3,...)
    nums= "a" * pagination_posts.paginator.num_pages
    pg=pagination_posts
    # End of setting pagination

    context = {'posts': posts,'tags':tags,'categories': categories,'pg':pg ,'nums':nums}
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
    # sending email to the user 
    try:
        send_mail("subscribed to a new category",
                'hello ,\nyou have just subscribed successfully to category '+category.cat_name,
                'settings.EMAIL_HOST_USER', [user.email],fail_silently=False,)
    except Exception :
                raise ValidationError("Couldn't send the message to the email ! ")        
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

            # get all the forbidden words as objects then get the post title and content that exist in the post request
            forbidden_words = ForbiddenWords.objects.all()
            content = request.POST.get("content")
            title = request.POST.get("title")

            # looping through the forbidden words 
            for word in forbidden_words :
                content_replaced = ""
                title_replaced=""
                #check if the forbidden word already exist in post content and post title 
                # if the word exists , we use the replace function to replace the forbidden word with asteriks 

                if word.forbidden_word in content : 
                    for char in word.forbidden_word :
                        content_replaced +="*"
                    content = content.replace(word.forbidden_word,content_replaced)
                if word.forbidden_word in title :
                    for char in word.forbidden_word :
                        title_replaced +="*"
                    title = title.replace(word.forbidden_word,title_replaced)

            obj = post_form.save(commit=False)
            #assign the new post content and title that we changed to the form 
            obj.content =content
            obj.title =title
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
    # get the post with its saved data
    post=Post.objects.get(id=post_id)
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
            #get all the forbidden words as objects then get the post title and content that exist in the post request

            forbidden_words = ForbiddenWords.objects.all()
            content = request.POST.get("content")
            title = request.POST.get("title")

             #check if the forbidden word already exist in post content and post title 
            # if the word exists , we use the replace function to replace the forbidden word with asteriks 

            for word in forbidden_words :
                replaced = ""
                title_replaced =""
                if word.forbidden_word in content : 
                    for char in word.forbidden_word :
                        replaced +="*"
                    content = content.replace(word.forbidden_word,replaced)
                if word.forbidden_word in title :
                    for char in word.forbidden_word :
                        title_replaced +="*"
                    title = title.replace(word.forbidden_word,title_replaced)
            
            obj = post_form.save(commit=False)
            #assign the new post content and title that we changed to the form 
            obj.content = content
            obj.title = title
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
            return redirect('landing')



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

    # print(post.dislikes.all.count)
    
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
        # Delete if dislikes greater than 10
        num_of_dislikes=post.dislikes.all().count()
 
        if num_of_dislikes == 10:
            post.delete()
            return redirect ('landing')
    
    # if the user clicked on the dislike button (already disliked), remove the dislike
    if is_dislike:
        post.dislikes.remove(request.user)
    
    post.save()
    
    return redirect('post',post_id)

# Add Comment
# Only logged in users can add comment on the post
@login_required(login_url='login')
def add_comment(request, post_id):
     # Interacted with specific post by id
    post = get_object_or_404(Post,id=post_id)
    # Retrieve all from forbidden words table
    forbidden_words = ForbiddenWords.objects.all()
    # Check for the request method then assign the user and text to the request user
    if request.method == 'POST':
        user = request.user
        comment_text = request.POST.get('text')
        # Retrieve all words from forbidden_words 
        for word in forbidden_words :
            replaced = ""
            # Check for the forbidden words in each comment and replace it with * 
            if word.forbidden_word in comment_text :
                for char in word.forbidden_word :
                    replaced +="*"
                comment_text = comment_text.replace(word.forbidden_word,replaced)
                 # Save the comments 
        Comment(user=user,post_id=post, comment_body=comment_text).save() 
    else:
        return redirect('post', post_id)
    return redirect('post', post_id)

# Add Reply
# Only logged in users can reply on the comment
@login_required(login_url='login')
def add_reply(request, post_id,comment_id):
     # Interacted with specific post by id
    post = Post.objects.get(id=post_id)
    # Retrieve all from comment table and assign them to the parent comment
    parent_comment = Comment.objects.get(id=comment_id)
    # Check for the request method then assign the user and reply to the request user
    if request.method == "POST":
        reply_body=request.POST.get('reply')
        author = request.user
        # Save the replies 
        Comment(user=author , post_id=post, comment_body=reply_body).save()
        reply_comment=Comment.objects.filter(comment_body=reply_body)
        reply_comment.parent=parent_comment
    else:
        return redirect('post', post_id)
    context={
        'post_id':post_id,
        'post':post,
        'reply_comment':reply_comment,
    }
    return render(request, 'dj_blog/post.html',context)
 




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

def addAvatar(request):
    form= AvatarForm()
    if request.method == "POST":
        form= AvatarForm(request.method ,request.FILES)
        if form.is_valid():
            account=Account.objects.get(user=request.user)
            account.avatar= request.FILES['avatar']
            account.save()
        return redirect('add-avatar')
    context = {'form':form}
    return render(request, 'dj_blog/add-avatar.html',context)