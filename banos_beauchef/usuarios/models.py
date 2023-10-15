from django.db import models
from django.contrib.auth.models import AbstractUser

# Clase del usuario que representa a un usuario en la base de datos.
# Los campos del usuario incluyen un id único con el cual indentificarlo,
# un nombre de usuario, una contraseña y un email,
# su nombre real y genero para representarlo, 
# un departamento al cual esta ligado,
# y una imagen ligada a su perfil.
class User(AbstractUser):
    departamentos=[('Plan Común','Plan Común'),('Astronomía','Astronomía'),
                   ('Física','Física'),('Geofísica','Geofísica'),
                   ('Geología','Geología'),('Civil','Civil'),
                   ('Biotecnología','Biotecnología'),('Computación','Computación'),
                   ('Eléctrica','Eléctrica'),('Industrial','Industrial'),
                   ('Matemática','Matemática'),('Mecánica','Mecánica'),
                   ('Minas','Minas'),('Química','Química'),
                   ('Magister/Doctorado','Magister/Doctorado')]
    genre = [('M','M'),('F','F'),('Otro', 'Otro')]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido_pat = models.CharField(max_length=50)
    apellido_mat = models.CharField(max_length=50)
    genero = models.CharField(max_length=5, choices=genre)
    departamento = models.CharField(max_length=30,choices=departamentos) 
    user_img = models.CharField(max_length=50,default="/static/img/profile1.png")
    
    def __str__(self):
        return str(self.username)