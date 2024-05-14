from django.db import models
from config.base_models import BaseAbstractModel
from apps.company.models import *
from apps.accounts.models import User
# Create your models here.

class config_tipo_sensor(models.Model):
    IdTipo = models.AutoField(primary_key= True)
    Nombre = models.CharField(default= "", max_length= 50, null= False, blank= True)
    Tipo_dato = models.CharField(default= "", null= "", blank= "", max_length=5)
    Icono = models.CharField(default= "", null= True, blank= False, max_length=50)
    Indice_widget = models.CharField(default= "", null= False, blank= False, max_length= 5)
    Rango_registros = models.CharField (default= "", null= True, blank= True, max_length= 10)
    Rango_tiempo = models.CharField ( default= "", null= False, blank= False, max_length= 20)
    Rango_max = models.CharField(default= "", null= False, blank= False, max_length= 20)
    Rango_min = models.CharField(default= "", null= False, blank= False, max_length= 20)
    
    fk_IdUSer = models.ForeignKey(User, null= False, on_delete= models.CASCADE, blank= False)
    def __str__(self):
        return self.Nombre
    
class dispositivo(BaseAbstractModel):
    ESTADOS = (
        ('habilitado', 'Habilitado'),
        ('deshabilitado', 'Deshabilitado'),
        ('nuevo', 'Nuevo'),
    )
    IdDispositivo = models.AutoField(primary_key=True)
    IdArea = models.ForeignKey(Area_trabajo, null=False, blank=False, on_delete= models.CASCADE)
    Modelo = models.CharField(default="", max_length=50, null=False, blank=False)
    MAC = models.CharField(default="", max_length=20, null=False, blank=False)
    Estado = models.CharField(default="nuevo", choices=ESTADOS, max_length=15, null=False, blank=False)
    
    def __str__(self):
        return self.Modelo
    
class sensor(BaseAbstractModel):
    ESTADOS = (
        ('habilitado', 'Habilitado'),
        ('deshabilitado', 'Deshabilitado'),
    )
    IdSensor = models.BigAutoField(primary_key=True)
    Nombre = models.CharField(("Nombre"), default="", max_length=30, blank=True, null=True)
    Licencia_sensor = models.CharField(default="", max_length=50, blank=False, null=False)
    IsAlive = models.BooleanField(default= True)
    Estado = models.CharField (default= 'habilitado', choices= ESTADOS, null= False, blank= False, max_length=15)
    #Llaves foraneas
    fk_IdTipo = models.ForeignKey(config_tipo_sensor, default="", blank=False, null=False, on_delete=models.CASCADE)
    fk_IdDispositivo = models.ForeignKey(dispositivo, default="", blank=False, null=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.Nombre
    
class register(BaseAbstractModel):
    IdRegistro = models.BigAutoField(('ID'), primary_key=True)
    fk_IdSensor = models.ForeignKey( sensor, null=False, on_delete= models.CASCADE)
    Valor = models.CharField( default='', max_length=50, null= True, blank= True)
    
    def __str__(self):
        return self.Valor
    
class registro_incidencias(BaseAbstractModel):
    IdRegistro = models.BigAutoField(primary_key= True)
    fk_IdSensor = models.ForeignKey(sensor, null= False, blank= False, on_delete=models.DO_NOTHING)
    Descripcion = models.CharField(default="", max_length=200, null= True, blank= True)
    
    def __str__(self):
        return self.Descripcion
    
