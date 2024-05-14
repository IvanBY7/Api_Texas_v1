from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Licencia)
class Licencia(admin.ModelAdmin):
    list_display = ('IdLicencia', 'Licencia','Fecha_registro', 'Fecha_vencimiento', 'Estado_licencia', 'Is_active')
    search_fields = ( 'IdLicencia',)
    list_filter = ('Estado_licencia', 'Is_active')