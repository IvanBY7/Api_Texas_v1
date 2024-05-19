from __future__ import unicode_literals
from django.db import models
from uuid import uuid4
from .managers import UserManager

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    is_active = models.BooleanField(default=False)  # Ensure the default is inactive
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.email

class Bitacora_moviminetos(models.Model):
    IdBitacora = models.BigAutoField(primary_key= True)
    Tipo_movimiento = models.CharField(_("Movimiento"), max_length=50)
    Fecha = models.DateField(_("Fecha"),auto_now=True, null=True, blank=True)
    Fecha = models.TimeField(_("Hora"),auto_now=True, null=True, blank=True)
    Bitacora = models.CharField(_("Bitacora"), max_length=200,  null=True, blank=True)
    
    fk_IdUser = models.ForeignKey(User, on_delete=models.DO_NOTHING)