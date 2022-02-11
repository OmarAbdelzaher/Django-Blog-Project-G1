from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post,name='post'),
    path('all-posts/',views.postPage,name='all-posts'),
    path('register/', views.registerpage , name='register' ),
    path('login/', views.loginpage , name='login' ),
    path('home/',views.home,name='home'),
]