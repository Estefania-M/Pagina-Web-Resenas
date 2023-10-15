from django.db import models
from bannos.models import Banno
from usuarios.models import User

# Modelo de las Reseñas, la cual contiene un id único, el id del baño a
# cual pertenece la reseña, el id del usuario el cual está creando la reseña,
# un contenido que son los comentarios del baño con un máximo de 300 caracteres.
# Además, posee valoraciones generales del baño, y valoraciones de otros aspectos
# los cuales son limpieza, utensilios, disponibilidad y comodidad. 
# Finalmente, se tiene un contador de valoraciones positivas y negativas.
class Resenna(models.Model):
    id_resenna = models.AutoField(primary_key=True) 
    banno = models.ForeignKey(Banno, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField(max_length=300)
    valoracion_general = models.FloatField()
    valoracion_limpieza = models.PositiveIntegerField(default=0)
    valoracion_utensilios = models.PositiveIntegerField(default=0)
    valoracion_disponibilidad = models.PositiveIntegerField(default=0)
    valoracion_comodidad = models.PositiveIntegerField(default=0)
    cantidad_de_valoracion_positiva = models.PositiveIntegerField(default=0)
    cantidad_de_valoracion_negativa = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.banno} User {self.usuario}"


# Modelo de los Comentarios a reseñas, la cual tiene un id único, un id
# de la reseña a la cual se esta respondiendo, un id del usuario, y un 
# contenido que será el texto del comentario con un máximo de 300 caracteres.
class Comentario(models.Model):
    id_comentario = models.AutoField(primary_key=True) 
    resena = models.ForeignKey(Resenna, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField(max_length=300)

    def __str__(self) -> str:
        return f"{self.id_comentario} {self.resena} User Comentario {self.usuario}"

