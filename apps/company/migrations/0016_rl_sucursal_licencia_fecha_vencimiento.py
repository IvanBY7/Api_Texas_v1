# Generated by Django 3.2.6 on 2024-05-19 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0015_auto_20240519_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='rl_sucursal_licencia',
            name='Fecha_vencimiento',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de vencimiento'),
        ),
    ]
