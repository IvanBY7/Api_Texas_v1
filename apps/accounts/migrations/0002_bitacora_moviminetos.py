# Generated by Django 3.2.6 on 2024-05-06 00:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bitacora_moviminetos',
            fields=[
                ('IdBitacora', models.BigAutoField(primary_key=True, serialize=False)),
                ('Tipo_movimiento', models.CharField(max_length=50, verbose_name='Movimiento')),
                ('Fecha', models.TimeField(auto_now=True, null=True, verbose_name='Hora')),
                ('Bitacora', models.CharField(blank=True, max_length=200, null=True, verbose_name='Bitacora')),
                ('fk_IdUser', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
