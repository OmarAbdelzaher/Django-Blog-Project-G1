from django.urls import path
from dj_admin import views 

urlpatterns = [
    path('starter/', views.starter,name='starter'),
    path('admins/' , views.showAdmins,name='admins'),
    path('promote/<id>',views.promoteUser,name="promote"),
    path('lock/<id>',views.lockUser,name="lock"),
    path('unlock/<id>',views.unlockUser,name="unlock"),
]