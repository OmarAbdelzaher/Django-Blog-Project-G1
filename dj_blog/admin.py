from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Category)
admin.site.register(PostTags)


class UserAccount(admin.ModelAdmin):
    list_display =['user','is_locked']
admin.site.register(Account,UserAccount)


class UserPanel(UserAdmin):
    list_display = ('id','username','email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff')
    add_fieldsets = (
        ('Personal Information', {
            'fields': ('username','first_name','last_name','email',
                       'password1', 'password2',)}
        ),
        ('Permissions',{
            'fields':( 'is_staff', 'is_active','is_superuser','date_joined')}),
    )

admin.site.unregister(User)
admin.site.register(User, UserPanel)
