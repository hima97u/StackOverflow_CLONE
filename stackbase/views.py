from django.shortcuts import render
from django.views.generic import ListView , DetailView , CreateView , UpdateView , DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin , LoginRequiredMixin
from . models import Question

def home(request):
    return render(request , 'home.html')

def about(request):
    return render(request , 'about.html')


#CRUD functionnality 

class QuestionListView(ListView):
    model = Question
    template_name = 'stackbase/question_list.html'
    context_object_name = 'questions'
    ordering = ['-created_at']
    
    
class QuestionDetailView(DetailView):
    model = Question
    template_name = 'stackbase/question_detail.html'
    context_object_name = 'question'


class QuestionCreateView(CreateView):
    model = Question
    template_name = 'stackbase/question_form.html'
    fields = ['title' , 'description']

    success_url = '/questions/'


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class QuestionUpdateView(UserPassesTestMixin , UpdateView):
    model = Question
    template_name = 'stackbase/question_form.html'
    fields = ['title' , 'description']

    success_url = '/questions/'


    def test_func(self):
        question = self.get_object()
        if self.request.user == question.user:
            return True
        else:
            return False



class QuestionDeleteview(LoginRequiredMixin , UserPassesTestMixin , DeleteView):
    model = Question
    template_name = 'stackbase/question_confirm_delete.html'
    success_url = '/questions/'

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.user:
            return True
        else:
            return False