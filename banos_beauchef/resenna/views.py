from django.shortcuts import render, redirect
import json

# Create your views here.
from resenna.models import Resenna, Comentario
from bannos.models import Banno, Ubicacion
from usuarios.models import User
from itertools import chain
from operator import attrgetter

def add_resennas(request): #the index view
    mis_bannos = Banno.objects.all()  # quering all todos with the object manager
    mis_ubicaciones = Ubicacion.objects.all()  # quering all resennas with the object manager
    if request.user.is_authenticated:
        mis_resennas = Resenna.objects.filter(usuario=request.user)  # quering all resennas with the object manager
    else:
        mis_resennas = Resenna.objects.filter(usuario=None)

    if request.method == "GET":
        return render(request, "resenna/add_resenna.html", {"resennas": mis_resennas, "bannos_all": mis_bannos, "ubicaciones": mis_ubicaciones})
    
    if request.method == "POST":  # revisar si el método de la request es POST
        if request.user.is_authenticated:
            if "resennaAdd" in request.POST:  # verificar si la request es para agregar una resenna (esto está definido en el button)
                usuario = request.user
                nombre_banno = request.POST["select_banno"]  # nombre del baño
                arr_banno = nombre_banno.split(sep=' ')
                if (arr_banno[1] == 'No'):
                    genero= arr_banno[1] + " " + arr_banno[2]
                    ubicacion = Ubicacion.objects.filter(piso=arr_banno[4], edificio=arr_banno[5], direccion=arr_banno[6])[0]
                else:
                    genero= arr_banno[1]
                    ubicacion = Ubicacion.objects.filter(piso=arr_banno[3], edificio=arr_banno[4], direccion=arr_banno[5])[0]
                banno = Banno.objects.filter(genero=genero, ubicacion=ubicacion.id)[0] # buscar el baño en la base de datos
                v_limpieza = int(request.POST["limpieza"]) #valoracion limpieza, ¿¿entrega enteros??
                v_comodidad = int(request.POST["comodidad"]) #valoracion comodidad
                v_disponibilidad = int(request.POST["personas"]) #valoracion disponibilidad
                v_utensilios  = int(request.POST["productos"]) #valoracion productos
                v_general = round((v_limpieza + v_comodidad + v_disponibilidad + v_utensilios)/4, 1)  #valoracion general, duda??
                contenido = request.POST["resenna"]  # contenido de la reseña

                #Se actualizan las valoraciones de los baños
                banno.annadir_val_bannos(request.POST)

                #Se crea la nueva reseña
                nueva_resenna = Resenna(banno=banno, 
                                        usuario=usuario, 
                                        contenido=contenido, 
                                        valoracion_general=v_general, 
                                        valoracion_limpieza=v_limpieza, 
                                        valoracion_utensilios=v_utensilios, 
                                        valoracion_disponibilidad=v_disponibilidad, 
                                        valoracion_comodidad=v_comodidad)    # Crear la resenna
                nueva_resenna.save()  # guardar la reseña en la base de datos.
                return redirect("/home")  # recargar la página.

def update_resennas(request, pk): 
    resenna = Resenna.objects.filter(id_resenna=pk).first()

    if request.method == "GET":
        return render(request, "resenna/update_resenna.html", {"resenna": resenna})
    
    if request.method == "POST":  # revisar si el método de la request es POST
        if request.user.is_authenticated:
            if "resennaUpdate" in request.POST:  # verificar si la request es para agregar una resenna (esto está definido en el button)
                nombre_banno = request.POST["select_banno"]  # nombre del baño
                arr_banno = nombre_banno.split(sep=' ', maxsplit=2)
                arr_ubicacion = arr_banno[2].split(sep=' ')
                ubicacion = Ubicacion.objects.filter(piso=arr_ubicacion[1], edificio=arr_ubicacion[2], direccion=arr_ubicacion[3])[0]
                banno = Banno.objects.filter(genero=arr_banno[1], ubicacion=ubicacion.id)[0] # buscar el baño en la base de datos
                resenna.valoracion_limpieza = int(request.POST["limpieza"]) #valoracion limpieza, ¿¿entrega enteros??
                resenna.valoracion_comodidad = int(request.POST["comodidad"]) 
                resenna.valoracion_disponibilidad = int(request.POST["personas"]) 
                resenna.valoracion_utensilios =  int(request.POST["productos"]) 
                resenna.valoracion_general = round((resenna.valoracion_limpieza + resenna.valoracion_comodidad + 
                                              resenna.valoracion_disponibilidad + resenna.valoracion_utensilios)/4, 1)
                resenna.contenido = request.POST["resenna"]  # contenido de la reseña

                val_anteriores = json.loads(request.POST["val_antiguas"])

                #Se actualizan las valoraciones de los baños
                banno.modificar_val_bannos(val_anteriores, request.POST)

                resenna.save()  # guardar la reseña en la base de datos.
                return redirect("/home") 

def recientes_resennas(request): 
    f_resennas = Resenna.objects.order_by("id_resenna")
    comentarios = Comentario.objects.all()

    if request.method == "GET":
        orden = "reciente"
        filtro_banno = "all"
        return render(request, "resenna/recientes_resennas.html", 
                      {"resennas": f_resennas, "orden": orden, "banno": filtro_banno, "comentarios": comentarios})
       
    if request.method == "POST":  # revisar si el método de la request es POST
        if "filtro-resenna" in request.POST:  
            f_orden = request.POST["select_orden"] 
            f_bannos = request.POST["select_bannos"]
            if(f_orden == "Más Antiguas"):
                orden = "antigua"
            else:
                orden = "reciente"
            if(f_bannos == "850"):
                ubicacion = Ubicacion.objects.filter(direccion=850)
                filtro_banno = "850"
            elif(f_bannos == "851"):
                ubicacion = Ubicacion.objects.filter(direccion=851)
                filtro_banno = "851"
            else:
                ubicacion = Ubicacion.objects.all()
                filtro_banno = "all"
            arr_filtro = []
            for u in ubicacion:
                banno = Banno.objects.filter(ubicacion=u.id)
                for b in banno:
                    arr_filtro.append(f_resennas.filter(banno=b.id))
                f_resenna = arr_filtro[0]
                for i in range(1, len(arr_filtro)):
                    f_resenna = sorted(chain(f_resenna, arr_filtro[i]),key=attrgetter('id_resenna'))

            return render(request, "resenna/recientes_resennas.html", 
                          {"resennas": f_resenna, "orden": orden, "banno": filtro_banno, "comentarios": comentarios})
        
        elif 'delete-resenna' in request.POST:
            id_reseña = request.POST['idR']
            deleteReseña = Resenna.objects.get(id_resenna=id_reseña)
            deleteReseña.delete()
            new_resennas = Resenna.objects.order_by("id_resenna")
            new_comentarios = Comentario.objects.all()
            orden = "reciente"
            filtro_banno = "all"

            return render(request, "resenna/recientes_resennas.html", 
                          {"resennas": new_resennas, "orden": orden, "banno": filtro_banno, "comentarios": new_comentarios})
        elif 'comentarioAdd' in request.POST:
            if request.user.is_authenticated:
                # El usuario está autenticado
                usuario = request.user
                id_reseña = request.POST['idR']
                resenna =  Resenna.objects.get(id_resenna=id_reseña)
                contenido = request.POST["comentario"]  

                nuevo_comentario = Comentario(usuario=usuario, resena=resenna, contenido=contenido)   
                nuevo_comentario.save()
                orden = "reciente"
                filtro_banno = "all"
                new_comentarios = Comentario.objects.all()

                return render(request, "resenna/recientes_resennas.html", 
                          {"resennas": f_resennas, "orden": orden, "banno": filtro_banno, "comentarios": new_comentarios})

            

#comentarios
def add_comentario(request, pk):
    resenna = Resenna.objects.get(id_resenna=pk)
    # El usuario está autenticado
    if request.user.is_authenticated:
        mis_comentarios = Comentario.objects.filter(usuario=request.user)
    else:
        mis_comentarios = Comentario.filter(usuario=None)

    usuario_resenna = resenna.usuario
    contenido_resenna = resenna.contenido

    if request.method == "GET":
        return render(request, "comentario/add_comentario.html", {"comentarios": mis_comentarios, 
                                                                  "usuario_resenna": usuario_resenna, 
                                                                  "contenido_resenna": contenido_resenna,})
    
    if request.method == "POST":
        if "comentarioAdd" in request.POST:
            usuario = request.user
            contenido = request.POST["comentario"]  # contenido del comentario

            nuevo_comentario = Comentario(resenna=resenna, usuario=usuario, contenido=contenido)  # Crear el comentario
            nuevo_comentario.save() # guardar el comentario en la base de datos.

            return redirect("/home") # recargar la página.

def update_comentario(request, pk1, pk2): 
    resenna = Resenna.objects.get(id_resenna=pk1)
    mi_comentario = Comentario.objects.get(id_comentario=pk2)

    usuario_resenna = resenna.usuario
    contenido_resenna = resenna.contenido
    contenido_comentario = mi_comentario.contenido

    if request.method == "GET":
        return render(request, "comentario/update_comentario.html", {"contenido_comentario": contenido_comentario, 
                                                                      "usuario_resenna": usuario_resenna, 
                                                                      "contenido_resenna": contenido_resenna})
    
    if request.method == "POST":
        if request.user.is_authenticated:
            if "comentarioUpdate" in request.POST:
                usuario = request.user
                contenido = request.POST["comentario"]  # contenido del comentario

                mi_comentario.contenido = contenido  # Actualizar el contenido del comentario existente
                mi_comentario.save()  # Guardar los cambios

                return redirect("/home")