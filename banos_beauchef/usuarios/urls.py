from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('profile/<int:pk>/',views.profile,name='profile'),
    path('logout/',views.logout_user,name='logout'),
    path('profiles/',views.profiles,name='profiles')
]     
