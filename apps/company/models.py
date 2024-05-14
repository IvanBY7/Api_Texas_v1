from django.db import models
from config.base_models import BaseAbstractModel
from apps.accounts.models import User
from apps.memberships.models import *

# Create your models here.
class config_web_empresa(models.Model):
    IdConfig = models.AutoField(primary_key= True, null= False )
    Element_fila = models.CharField(('Elementos por fila'), max_length=2, null= True, blank= True)
    Color_estable = models.CharField(('Color estable'), max_length=8, null= True, blank= True)
    Color_advertencia = models.CharField(('Color advertencia'), max_length=8, null= True, blank= True)
    Color_urgencia = models.CharField(('Color urgencia'), max_length=8, null= True, blank= True)
    
    def __int__(self):
        return self.IdConfig

class  company(BaseAbstractModel):
    IdEmpresa = models.AutoField(primary_key= True)
    Nombre_Empresa = models.CharField(('Empresa'), default="", null= False, max_length=50)
    Url_img = models.ImageField(('Imagen'), upload_to='imagenes/', null=True, blank=True)
    fk_config = models.ForeignKey(config_web_empresa, on_delete=models.DO_NOTHING, null=True, blank=True)
    def __str__(self): 
        return self.Nombre_Empresa
    
class Rl_user_company(models.Model):
    IdRelacion = models.AutoField(primary_key= True)
    fk_IdUsuario = models.ForeignKey(User, on_delete=models.CASCADE, null= False, blank= False)
    fk_IdEmpresa = models.ForeignKey(company, on_delete=models.CASCADE, null= True, blank= True)
    def __int__(self):
        return self.IdRelacion
    


class region(BaseAbstractModel):
    IdRegion = models.AutoField(primary_key= True, null= False)
    Nombre_region = models.CharField(('Region'), default= "", max_length=50, null=False, blank=False)
    Ubicacion = models.CharField(('Ubicación'), default= "", max_length=150, null= True, blank= True)
    Telefono = models.CharField(default= "", max_length=15, null= True, blank=True)
    Correo = models.CharField(default= "", max_length=50, null=True, blank= True)
    fk_IdEmpresa = models.ForeignKey(company, null= True, blank= True, on_delete= models.CASCADE)

    def __str__(self):
        return self.Nombre_region
    
class Sucursal(BaseAbstractModel):
    
    IdSucursal = models.AutoField(primary_key= True)
    Nombre_sucursal = models.CharField(('Sucursal'), default= "", max_length=50, null= False, blank= False)
    Ubicacion = models.CharField(default= "", max_length=150, null= True, blank= True)
    Telefono = models.CharField(default= "", max_length=15, null= True, blank=True)
    Correo = models.CharField(default= "", max_length=50, null=True, blank= True)
    Is_active = models.BooleanField(default=True)
    Ruta_img = models.CharField(('img'), default= "", null= True, blank= True, max_length=200)
    
    # Llaves foraneas
    fk_IdRegion = models.ForeignKey(region, null= False, blank= False, on_delete=models.CASCADE)
    
    def __srt__(self):
        return self.Nombre_sucursal
    
class Rl_sucursal_licencia(models.Model):
    Id_relacion = models.AutoField(primary_key= True)
    fk_IdSucursal = models.ForeignKey(Sucursal, null= False, blank= False, on_delete= models.CASCADE)
    fk_IdLicencia = models.ForeignKey(Licencia, null= False, blank= False, on_delete= models.CASCADE)
    
    def __srt__(self):
        return self.Id_relacion
    
class Area_trabajo(models.Model):
    IdArea = models.AutoField(primary_key= True)
    Nombre_zona = models.CharField(default= "", null= False, max_length=50 )
    Is_active = models.BooleanField(default= True)
    fk_IdSucursal = models.ForeignKey(Sucursal, null= False, on_delete= models.CASCADE)
    
    def __srt__(self):
        return self.Nombre_zona