# Generated by Django 3.2.6 on 2024-05-13 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20240513_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rl_user_company',
            name='fk_IdEmpresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.company'),
        ),
    ]