from django.shortcuts import render, redirect
from bannos.models import Banno
from bannos.models import Ubicacion
from django.db import models
from resenna.models import Resenna

    # Create your views here.
    # Vamos a crear forms para poder agreagar/modificar/delete bannos
    # más facilmente


def add_banno(request):
    mis_bannos = Banno.objects.all()

    if request.method == "GET":
        return render(request, "addBanno", {"parametros"})

    if request.method == "POST":
        # Enviar datos de un baño

        if "bannoAdd" in request.POST:
            nombre = request.POST("nombre")
            descripcion = request.POST("descripcion")
            ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
            genero = models.CharField(max_length=10, choices=[("Masculino", "Masculino"), ("Femenino","Femenino"), ("No binario","No binario")])
            valoracion_limpieza = 0
            valoracion_utensilios = 0
            valoracion_disponibilidad = 0
            valoracion_comodidad = 0
            valoracion_general = 0
            return redirect("/addBanno")




def add_ubicacion(request):
    # Enviar datos de un baño
    if request.method == "GET":
        return render(request, "addUbicacion", {"parametros"})

    if request.method == "POST":
        piso = request.POST("piso")
        edificio = request.POST("edificio")
        direccion = models.PositiveSmallIntegerField(null=True, choices=[(850, 850), (851, 851)])
        return redirect("/addUbicacion")

def recommendedBannos(request):
    bannosRec = Banno.objects.order_by("-valoracion_general")[:5]
    if request.method == "GET":
        return render(request, "bannos/recommendedBannos.html", {"bannos":bannosRec})
    
    if request.method == "POST":
        filtro = request.POST["filtro"]
        bannosRec = Banno.objects.order_by(f"-valoracion_{filtro}")[:5]
        return render(request, "bannos/recommendedBannos.html", {"bannos":bannosRec})


def home(request):
    user = request.user
    pkO = user.id
    bannos = Banno.objects.all()
    resennas = Resenna.objects.order_by("-id_resenna")[:5] #ultimas 5 reseñas
    context = {'user':user,'bannos': bannos, 'pk':pkO, 'resennas': resennas}
    if request.method == "GET":
        return render(request, "home/home.html", context)


def ochocincuenta(request):
    user = request.user
    pkO = user.id
    bannos = Banno.objects.filter(ubicacion__direccion="850")
    context = {'user':user,'bannos': bannos, 'pk':pkO}

    if request.method == "GET":
        return render(request, "home/850.html", context)

def ochocincuentayuno(request):
    user = request.user
    pkO = user.id
    bannos = Banno.objects.filter(ubicacion__direccion="851")
    context = {'user':user,'bannos': bannos, 'pk':pkO}
    if request.method == "GET":
        return render(request, "home/851.html", context)

def bannoProfile(request, pk):
    banno = Banno.objects.get(id=pk)
    resennas = Resenna.objects.filter(banno=banno)
    if request.method == "GET":
        return render(request, "bannos/bannoPage.html", {"banno": banno, "resennas": resennas})


