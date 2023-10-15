from django.contrib import admin

# Register your models here.
from resenna.models import Resenna
from resenna.models import Comentario
from bannos.models import Banno
from bannos.models import Ubicacion

# Register your models here.
admin.site.register(Resenna)
admin.site.register(Comentario)
admin.site.register(Banno)
admin.site.register(Ubicacion)