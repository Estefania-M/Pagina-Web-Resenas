from django.urls import path
from . import views



urlpatterns = [

    path('addBanno/', views.add_banno, name='Agregar Baño'),
    path('addUbicacion/', views.add_ubicacion, name='Agregar Ubicacion'),
    path('recommendedBannos/', views.recommendedBannos, name= "recommendedBannos"),
    path('bannoProfile/<int:pk>/', views.bannoProfile, name='Perfil de Baño'),
    path('home/', views.home, name= "home"),
    path('850/', views.ochocincuenta, name= "850"),
    path('851/', views.ochocincuentayuno, name= "851"),
]
