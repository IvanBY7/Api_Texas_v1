from django.db import models

# Create your models here.
class Licencia(models.Model):
    ESTADOS = (
        ('vigente', 'Vigente'),
        ('vencido', 'Vencido'),
        ('por_vencer', 'Por Vencer'),
        ('disponible', 'Disponible'),
    )
    
    IdLicencia = models.AutoField(primary_key= True)
    Licencia = models.CharField(('Licencia'), default= "", max_length=100, null= False, blank= False)
    Fecha_registro = models.DateTimeField(('Fecha de registro'), auto_now_add=True, null=False, blank=False)
    Fecha_vencimiento = models.DateTimeField(('Fecha de vencimiento'), null=True, blank=True)
    Estado_licencia = models.CharField(default= 'disponible', choices=ESTADOS, null=False, blank= False, max_length=50)
    Is_active = models.BooleanField(default=True)
    
    
    
    def __srt__(self):
        return self.Estado_licencia