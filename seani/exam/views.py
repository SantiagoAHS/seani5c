from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Exam, Breakdown
from django.contrib.auth.decorators import login_required

from .forms import CandidateForm
# Create your views here.
@login_required 
def home(request):
    user = request.user
    if user.is_superuser:
        return redirect('admin:index')
    return render(request, 'exam/home.html',{'user':user})

@login_required
def question(request, m_id, q_id=1):
    exam = request.user.exam
    if request.method == 'POST':
        answer = request.POST.get('answer')
        questions = exam.breakdown_set.filter(question__module_id=m_id)
        if q_id > len(questions) or q_id < 1:
            return redirect('exam:home')  # Si el ID de la pregunta está fuera de rango, redirige a la página de inicio
        question = questions[q_id - 1]
        question.answer = answer
        question.save()
        if q_id == len(questions):  # Si es la última pregunta, redirige a la página de inicio
            exam.compute_score_by_module(m_id)
            exam.compute_score()
            return redirect('exam:home')
        else:
            return redirect('exam:question', m_id, q_id + 1)
    else:
        questions = exam.breakdown_set.filter(question__module_id=m_id)
        if q_id > len(questions) or q_id < 1:
            return redirect('exam:home')  # Si el ID de la pregunta está fuera de rango, redirige a la página de inicio
        question = questions[q_id - 1].question
        answer = questions[q_id - 1].answer
        return render(request, 'exam/question.html', {
            'question': question,
            'answer': answer,
            'm_id': m_id,
            'q_id': q_id
        })

@login_required
def add_candidate(request):
    if request.method =='POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            #Recibir datos
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email= form.cleaned_data['email']
            password = form.cleaned_data['password']
            career = form.cleaned_data['career']
            stage = form.cleaned_data['stage']

            #Crear usuario
            user = User.objects.create_user(username,email,password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            #Crear examne 
            exam = Exam.objects.create(
                user=user,
                career=career,
                stage=stage,)
            
            #llenar examen
            exam.set_modules()
            exam.set_questions()
            return HttpResponse("Usuario y examnet creado")
    form = CandidateForm
    return render(request, 'exam/add_candidate.html',{'form':form})

