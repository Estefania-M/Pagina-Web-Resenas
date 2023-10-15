from django.shortcuts import render, redirect
from usuarios.models import User
from django.contrib.auth import authenticate, login as logins, logout as logouts
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from resenna.models import Resenna

# Recibe el formulario y registra a un usuario dentro de la base de datos
def register_user(request):
    if request.method == 'GET': #Si estamos cargando la página
     return render(request, "usuarios/register.html") #Mostrar el template

    elif request.method == 'POST': #Si estamos recibiendo el form de registro
     #Tomar los elementos del formulario que vienen en request.POST
     usuario = request.POST['nombre_usuario']
     #Si el username ya fue ocupado, notificar
     if(User.objects.filter(username=usuario).exists()):
      messages.success(request,("Usuario ya ocupado"))
      return redirect('register')
     contraseña = request.POST['contraseña']
     mail = request.POST['mail']
     nombre = request.POST['nombre']
     apellido_pat = request.POST['apellido_pat']
     apellido_mat = request.POST['apellido_mat']
     genero = request.POST['genre']
     departamento = request.POST['departamento']

     #Crear el nuevo usuario
     user = User.objects.create_user(username=usuario, 
                                     password=contraseña, 
                                     email=mail, 
                                     nombre=nombre, 
                                     apellido_pat=apellido_pat,
                                     apellido_mat=apellido_mat,
                                     genero=genero,
                                     departamento=departamento)
     # Redireccionar la página 
     return HttpResponseRedirect("/login")
    
# Permite acceder a la cuenta de un usuario
def login_user(request):
  # Se llega al template de login
  if request.method == 'GET':
    return render(request, "usuarios/login.html")
  # Aca se hace un intento de acceder a la cuenta
  elif request.method == 'POST' and 'log' in request.POST:
    usuario = request.POST['nombre_usuario']
    password = request.POST['contraseña']
    user = authenticate(request, username=usuario, password=password)
    # Si el usuario existe en la base de datos y la contraseña es correcta
    if user is not None:
      logins(request,user)
      return redirect('home')
    # Nombre o contraseña incorrecta
    # Informar casos: si usuario no existe | contraseña mala
    else:
      messages.success(request,("Error al autenticar"))
      return redirect('login')
  


# Permite mostrar información de un usuario
def profile(request,pk):
  user = request.user
  pkO = user.id
  if request.user.is_authenticated:
    if pkO==pk:
      if request.method=='POST':
        # Capturamos la intención de un usuario de cambiar su foto
        if 'cambiofoto' in request.POST:
          # Se obtiene la imagen nueva
          src = request.POST['srcInput']
          # Se cambia en la base de datos
          user.user_img = src
          # Se actualiza
          user.save()
        # Eliminar una reseña 
        elif 'delete-resenna' in request.POST:
          id_reseña = request.POST['idR']
          deleteReseña = Resenna.objects.get(id_resenna=id_reseña)
          deleteReseña.delete()
    else:
      user = User.objects.get(id=pk)
  else:
    user = User.objects.get(id=pk)
    print(user.is_authenticated)
  resennas = Resenna.objects.filter(usuario=user)
  context = {'user':user,'resennas': resennas, 'pk':pkO}
  return render(request,'usuarios/profile.html',context)


# Permite ver todos los usuarios registrados en la página
def profiles(request):
  users = User.objects.all()
  return render(request,'usuarios/profiles.html',{'users':users})

@login_required
# Permite hacer logout/cerrar sesión.
def logout_user(request):
  logouts(request)
  return redirect('home')