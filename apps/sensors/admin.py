from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(register)
class register(admin.ModelAdmin):
    list_display = ('IdRegistro', 'fk_IdSensor', 'Valor',)
    search_fields = ( 'Valor', 'IdSensor')
    list_filter = ('fk_IdSensor', )
    
    
@admin.register(sensor)
class sensor(admin.ModelAdmin):
    list_display = ('IdSensor', 'Nombre', 'fk_IdDispositivo', 'Estado')
    search_fields = ( 'Nombre',)
    list_filter = ('fk_IdDispositivo',  'Estado')
    
@admin.register(config_tipo_sensor)
class config_tipo_sensor(admin.ModelAdmin):
    list_display = ('IdTipo', 'Nombre', 'Tipo_dato',  'Indice_widget')
    search_fields = ( 'Tipo_dato', 'Nombre', 'fk_IdUser')
    
@admin.register(dispositivo)
class dispositivo(admin.ModelAdmin):
    list_display = ('IdDispositivo', 'IdArea', 'Modelo',  'Estado',)
    search_fields = ( 'IdArea', 'Modelo',)
    list_filter = ('Estado',)
    
@admin.register(registro_incidencias)
class registro_incidencias(admin.ModelAdmin):
    list_display = ('IdRegistro', 'fk_IdSensor', 'Descripcion',)
    list_filter = ('fk_IdSensor',)