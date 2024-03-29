# Generated by Django 5.0.2 on 2024-02-22 18:38

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_alter_module_options_alter_question_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='Imagen de la pregunta'),
        ),
    ]
