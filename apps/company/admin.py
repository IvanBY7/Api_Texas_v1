from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(company)
class company(admin.ModelAdmin):
    list_display = ('IdEmpresa', 'Nombre_Empresa','Url_img')
    search_fields = ( 'Fecha', 'Nombre_Empresa')
    
@admin.register(Rl_user_company)
class Rl_user_company(admin.ModelAdmin):
    list_display = ('IdRelacion', 'fk_IdUsuario','fk_IdEmpresa')
    search_fields = ( 'fk_IdUsuario', 'fk_IdEmpresa')
    
@admin.register(config_web_empresa)
class config_web_empresa(admin.ModelAdmin):
    list_display = ('IdConfig','Element_fila', 'Color_estable', 'Color_advertencia', 'Color_urgencia')
    
@admin.register(region)
class region(admin.ModelAdmin):
    list_display = ('IdRegion', 'Nombre_region','Correo', 'fk_IdEmpresa')
    search_fields = ( 'Fecha', 'Nombre_region')
    
@admin.register(Sucursal)
class Sucursal(admin.ModelAdmin):
    list_display = ('IdSucursal', 'Nombre_sucursal','Correo', 'fk_IdRegion', 'Is_active')
    search_fields = ('IdSucursal', 'Fecha', 'Nombre_sucursal', 'fk_IdRegion', )
    
@admin.register(Rl_sucursal_licencia)
class Rl_sucursal_licencia(admin.ModelAdmin):
    list_display = ('Id_relacion', 'fk_IdSucursal','fk_IdLicencia', )
    search_fields = ('fk_IdSucursal', 'fk_IdLicencia', )

@admin.register(Area_trabajo)
class Area_trabajo(admin.ModelAdmin):
    list_display = ('IdArea', 'Nombre_zona','fk_IdSucursal', 'Is_active',)
    search_fields = ('Nombre_zona', 'fk_IdSucursal', )