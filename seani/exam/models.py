from django.db import models
from django.contrib.auth.models import User
from career.models import Carrer
from library.models import Module, Question


# Create your models here.
class Stage(models.Model):

    stage = models.IntegerField(
        verbose_name =  "Etapa",
        max_length=2
        )
    application_date = models.DateField(
        verbose_name = "Fecha de aplicacion"
    )
    
    @property
    def year(self):
        return self.application_date.year
    
    @property
    def month(self):
        months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio' , 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

        return months[self.application_date.month - 1]
    
    def __str__(self):
        return f"{ self.stage } - {self.month } - { self.year }"
    
    class Meta:
        verbose_name = "Etapa"
        verbose_name_plural = "Etapas"

class Exam(models.Model):
    user = models.OneToOneField(User,
                                on_delete = models.CASCADE,
                                verbose_name = "Usuario")
    stage = models.ForeignKey(Stage,
                              on_delete = models.CASCADE,
                              verbose_name = "Etapa")
    career = models.ForeignKey(Carrer,
                              on_delete = models.CASCADE,
                              verbose_name = "Carrera")
    modules = models.ManyToManyField(Module,
                                     through='ExamModule',
                                     verbose_name = "Modulos")
    question = models.ManyToManyField(
        Question,
        verbose_name="preguntas"
    )
    score = models.FloatField(verbose_name = "Calificación",
                              default = 0.0)
    created = models.DateTimeField(
        auto_now_add = True, 
        verbose_name = 'Fecha de Creacion')
    updated = models.DateTimeField(auto_now = True,
                                   verbose_name = 'Fecha de Actualizacion')
    
    def set_modules(self):
        for module in Module.objects.all():
            self.modules.add(module)

    def set_questions(self):
        for module in self.modules.all():
            for question in module.question_set.all():
                Breakdown.objects.create(
                    exam = self,
                    question = question,
                    correct = question.correct
                )

    def compute_score(self):
        score = 0.0
        for exammodule in self.exammodule_set.all():
            score += exammodule.score
        if self.exammodule_set.count() != 0:
            self.score = score / self.exammodule_set.count()
        else:
            self.score = 0.0  # Manejar el caso cuando no hay módulos asociados al examen
        self.save()

    def compute_score_by_module(self, m_id):
        score = 0.0
        questions = self.breakdown_set.filter(question__module_id=m_id)
        question_count = questions.count()

        if question_count > 0:
            for question in questions:
                if question.answer == question.correct:
                    score += 10
            module = self.exammodule_set.get(module_id=m_id)
            module.score = score / question_count
            module.save()
        else:
            # Manejar el caso cuando no hay preguntas asociadas al módulo
            module = self.exammodule_set.get(module_id=m_id)
            module.score = 0.0
        module.save()

    def __str__(self):
        return f"{self.user} - {self.career}: {self.score}"
    
    class Meta:
        verbose_name = "Examen",
        verbose_name_plural = "Examenes"


class ExamModule(models.Model):
    exam = models.ForeignKey(Exam,
                              on_delete = models.CASCADE,
                              verbose_name = "Examen")
    module = models.ForeignKey(Module,
                              on_delete = models.CASCADE,
                              verbose_name = "Modulo")
    active = models.BooleanField(default = True,
                                 verbose_name = "Activo")
    score = models.FloatField(default = 0.0,
                              verbose_name = "Calificacion")
    
    def __str__(self) :
        return f"{self.module} - {self.score}"



class Breakdown(models.Model):
    exam = models.ForeignKey(Exam,
                              on_delete = models.CASCADE,
                              verbose_name = "Examen")
    question = models.ForeignKey(Question,
                                 on_delete = models.CASCADE,
                                 verbose_name = "Pregunta")
    answer = models.CharField(max_length=5,
                              verbose_name = "Respuesta",
                              default = '-')
    correct = models.CharField(max_length = 5,
                                  verbose_name = "Correcta",
                                  default = '-')
    
    def __str__(self) :
        return f"{self.question} - {self.answer} - {self.correct}"  
    
    class Meta:
        verbose_name = "Desglose"
        verbose_name_plural = "Desglosos"