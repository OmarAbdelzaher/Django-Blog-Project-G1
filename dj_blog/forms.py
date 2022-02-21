from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm ,UsernameField
from django.core.exceptions import ValidationError

# register form based on built-in usercreationform
class RegistrationForm(UserCreationForm):
    email =  forms.EmailField(required=True,max_length=100)
    class Meta:
        model = User
        fields =['username','email','password1','password2']
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        email =cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exist !")

# login form inherits from built-in authenticationform 
class LoginForm(AuthenticationForm): 
    username = UsernameField( widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username..'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password...'}))

# Post Form 
class PostForm(forms.ModelForm):
    content = forms.TextInput(attrs={'class': 'form-control'})
    class Meta:
        model = Post
        fields = ['title','picture','content','category','tag']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
            'content':forms.TextInput(attrs={'class': 'form-control'}),
            'category' : forms.Select(attrs={'class':'form-control'}),
        }

# Tags Form    
class TagsForm(forms.ModelForm):
    class Meta:
        model = PostTags
        fields = ['tag_name']
        widgets = {
            'tag_name': forms.TextInput(attrs={'class': 'form-control', 'data-role': 'tagsinput','required':'False'})
        }
        
# Comment Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_body', )
        widgets = {
        "comment_body":forms.TextInput(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'comment here ...',
        'rows': '4',
    })}
            
# Category Form
class CategoryForm(forms.ModelForm):
    cat_name = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = Category
        fields = ('cat_name',)
    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()
        cat_name = cleaned_data.get("cat_name")
        if Category.objects.filter(cat_name = cat_name).exists():
            raise ValidationError("Category Already exists !")

# Forbidden Words Form
class ForbiddenWordsForm(forms.ModelForm):
    forbidden_word=forms.CharField(widget=forms.TextInput())
    class Meta:
        model = ForbiddenWords
        fields = ('forbidden_word',)
    def clean(self):
        cleaned_data = super(ForbiddenWordsForm, self).clean()
        forbidden_word = cleaned_data.get("forbidden_word")
        if ForbiddenWords.objects.filter(forbidden_word = forbidden_word).exists():
            raise ValidationError("This Word Already exists !")
    
class AvatarForm(forms.ModelForm):
    
    class Meta:
        model= Account
        fields= ('avatar',)
        widget={
         'avatar': forms.FileInput(attrs={'class': 'form-control'}),    
        }