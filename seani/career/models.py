from django.db import models

# Create your models here.
class Carrer(models.Model):
    LEVELS=[
        ('ing','Ingenieria'),
        ('TSU','Tecnico Superior Universitario'),
        ('M','Maestria')
    ]

    name = models.CharField(max_length = 200, verbose_name = 'Nombre')
    short_name = models.CharField(max_length = 20, verbose_name = 'Abreviaturas')
    level = models.CharField(max_length=10, choices = LEVELS , verbose_name='Nivel') 

    def __str__(self):
        return f"{ self.level } - {self.short_name}"
    
    class Meta:
        verbose_name = 'carrera'
        verbose_name_plural='carerras'
