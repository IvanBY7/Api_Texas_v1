# Generated by Django 3.2.6 on 2024-05-16 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0012_alter_area_trabajo_fk_idsucursal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sucursal',
            name='Ruta_img',
        ),
        migrations.AddField(
            model_name='sucursal',
            name='ImagenSucursal',
            field=models.ImageField(blank=True, null=True, upload_to='sucursales/', verbose_name='Imagen'),
        ),
    ]
