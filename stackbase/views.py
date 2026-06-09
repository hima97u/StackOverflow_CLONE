from django.shortcuts import render
from django.views.generic import ListView
from . models import Question

def home(request):
    return render(request , 'home.html')

def about(request):
    return render(request , 'about.html')


#CRUD functionnality 

class QuestionListView(ListView):
    model = Question
    template_name = 'stackbase/question_list.html'
    cotext_object_name = 'questions'
    ordering = ['-created_at']
    
    