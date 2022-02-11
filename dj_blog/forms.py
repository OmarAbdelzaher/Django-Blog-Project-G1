from django import forms
from .models import User

class CreateUserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    password =forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','email','password')
    def clean(self):
        # clean method for validation and ordering the data 
        cleaned_data = super(CreateUserForm, self).clean()
        username = cleaned_data.get("username")
        email =cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        #validate username 
        if len(username) < 3 :
            raise forms.ValidationError(('Username must be more than 3'))
        #validate password 
        if len(password) < 8:
            raise forms.ValidationError(('Password must be more than 8'))
        #checking existence email 
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(('Email is already exist'))
        #validate matching password 
        if password != confirm_password:
            raise forms.ValidationError((
                "Your current and confirm password do not match."))

