from django.db import models

# Create your models here.


class Stage(models.Model):

    stage = models.IntegerField(
        verbose_name = "Etapa")
    aplication_date = models.DateField(
        verbose_name="Fechha de Aplicacion")

    @property
    def year(self):
        return self.aplication_date.year
    
    @property
    def month(self):
        months = ['enero','febrero','marzo','abril','mayo','julio','junio','agosto','septiembre','octubre','noviembre','diciembre']
        return months[self.aplication_date.month - 1]
    
    
    def __str__(self):
        return f"{ self.stage}-{ self.month }-{self.year}"

    class Meta:
        verbose_name="etapa"
        verbose_name_plural="etapas"