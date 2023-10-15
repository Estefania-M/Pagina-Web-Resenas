from django.db import models


# Modelo de las ubicaciones en las que se pueden encontrar los baños.
class Ubicacion(models.Model):
    # Id para identificar a cada ubicación posible.
    id = models.AutoField(primary_key=True)

    # Dirección de la ubicación, es decir, si se encuentra en 850 u 851 de la FCFM.
    direccion = models.PositiveSmallIntegerField(null=True, choices=[(850, 850), (851, 851)])

    # Edificio de la facultad en el que se encuentra.
    edificios = ["Escuela", "Física", "Minas", "Justicia Espada", "Eléctrica", "Geología", "Civil", #850
                  "Norte", "Oriente", "Poniente", "Subterraneo"] # 851
    edificio = models.CharField(max_length=250, choices= [(x, x) for x in edificios])

    # Piso en el que se encuentra.
    piso = models.IntegerField()

    def __str__(self) -> str:
        return f"Piso {self.piso} {self.edificio} {self.direccion}"
    
# Modelo de los baños que a los que se les podrá hacer reseñas.
class Banno(models.Model):
    # Número para identificar a cada baño.
    id = models.AutoField(primary_key=True) 
    
    # Descripción del baño
    descripcion = models.TextField(blank=True)

    # Id de la Ubicación en la que se encuentra un baño
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    
    # Género del baño, este puede ser "Masculino", "Femenino" o "No binario"
    genero = models.CharField(max_length=10, choices=[("Masculino", "Masculino"), ("Femenino","Femenino"), ("No binario","No binario")])

    # Valoración de la limpieza del baño
    valoracion_limpieza = models.FloatField()

    # Valoración de los utensilios del baño
    valoracion_utensilios = models.FloatField()

    # Valoración de la disponibilidad del baño
    valoracion_disponibilidad = models.FloatField()

    # Valoración de la comodidad del baño
    valoracion_comodidad = models.FloatField()

    # Promedio del las valoración del baño
    valoracion_general = models.FloatField(default=1.0)

    # Número de reseñas del baño
    num_resennas = models.IntegerField(default=0)

    # imagena
    banno_img = models.CharField(max_length=50,default="/static/assets/images/b1.jpg")



    def __str__(self):
        return f"Baño {self.genero} {self.ubicacion}"
    

    # Método para añadir las valoraciones de una reseña nueva al baño.
    # Recibe las valoraciones en un diccionario.
    def annadir_val_bannos(self, valoracionesDict):

        comodidad = int(valoracionesDict["comodidad"])
        disponibilidad = int(valoracionesDict["personas"])
        limpieza = int(valoracionesDict["limpieza"])
        utensilios = int(valoracionesDict["productos"])

        # Si el baño no tiene reseñas, se le asignan las valoraciones de la reseña.
        if self.num_resennas == 0:
            self.valoracion_comodidad = comodidad
            self.valoracion_disponibilidad = disponibilidad
            self.valoracion_limpieza = limpieza
            self.valoracion_utensilios = utensilios
            self.valoracion_general = round((comodidad + disponibilidad + limpieza + utensilios) / 4, 1)

        # Si ya tenía reseñas, se calculan las nuevas valoraciones como el promedio de las valoraciones de todas las reseñas del baño.
        else:
            nuevaComodidad = (self.valoracion_comodidad * self.num_resennas + comodidad) / (self.num_resennas + 1)
            nuevaDisponibilidad = (self.valoracion_disponibilidad * self.num_resennas + disponibilidad) / (self.num_resennas + 1)
            nuevaLimpieza = (self.valoracion_limpieza * self.num_resennas + limpieza) / (self.num_resennas + 1)
            nuevaUtensilios = (self.valoracion_utensilios * self.num_resennas + utensilios) / (self.num_resennas + 1)
            nuevaGeneral = (nuevaComodidad + nuevaDisponibilidad + nuevaLimpieza + nuevaUtensilios) / 4
            self.valoracion_comodidad = round(nuevaComodidad, 1)
            self.valoracion_disponibilidad = round(nuevaDisponibilidad, 1)
            self.valoracion_limpieza = round(nuevaLimpieza, 1)
            self.valoracion_utensilios = round(nuevaUtensilios, 1)
            self.valoracion_general = round(nuevaGeneral, 1)
        
        self.num_resennas += 1
        self.save()

    # Método para modificar las valoraciones de un baño al cambiar las valoraciones de una reseña.
    # Recibe las valoraciones nuevas y antiguas de la reseña en dos diccionarios.
    def modificar_val_bannos(self, valoracionesAnt, valoracionesNuevas):

        comodidadAnt = int(valoracionesAnt["comodidad"])
        disponibilidadAnt = int(valoracionesAnt["personas"])
        limpiezaAnt = int(valoracionesAnt["limpieza"])
        utensiliosAnt = int(valoracionesAnt["productos"])
        comodidadNueva = int(valoracionesNuevas["comodidad"])
        disponibilidadNueva = int(valoracionesNuevas["personas"])
        limpiezaNueva = int(valoracionesNuevas["limpieza"])
        utensiliosNueva = int(valoracionesNuevas["productos"])

        nuevaComodidad = self.valoracion_comodidad + round((comodidadNueva - comodidadAnt) / self.num_resennas, 1)
        nuevaDisponibilidad = self.valoracion_disponibilidad + round((disponibilidadNueva - disponibilidadAnt) / self.num_resennas, 1)
        nuevaLimpieza = self.valoracion_limpieza + round((limpiezaNueva - limpiezaAnt) / self.num_resennas, 1)
        nuevaUtensilios = self.valoracion_utensilios + round((utensiliosNueva - utensiliosAnt) / self.num_resennas, 1)
        nuevaGeneral = (nuevaComodidad + nuevaDisponibilidad + nuevaLimpieza + nuevaUtensilios) / 4
        self.valoracion_comodidad = round(nuevaComodidad, 1)
        self.valoracion_disponibilidad = round(nuevaDisponibilidad, 1)
        self.valoracion_limpieza = round(nuevaLimpieza, 1)
        self.valoracion_utensilios = round(nuevaUtensilios, 1)
        self.valoracion_general = round(nuevaGeneral, 1)
        self.save()
