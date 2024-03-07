from django.urls import path

from . import views


app_name ='exam'
urlpatterns = [
    path('create/', views.add_candidate, name='add_candidate')
]