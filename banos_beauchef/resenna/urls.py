from django.urls import path
from . import views

urlpatterns = [
    path('add_resenna/', views.add_resennas, name='add_resennas'),
    path('update_resenna/<int:pk>/', views.update_resennas, name='update_resennas'),
    path('recientes_resennas/', views.recientes_resennas, name='recientes_resennas'),
    path('add_comentario/<int:pk>', views.add_comentario, name='add_comentario'),
    path('update_comentario/<int:pk1>/<int:pk2>', views.update_comentario, name='update_comentario'),
]     