from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post,name='post'),
    path('all-posts/',views.postPage,name='all-posts')
]