from django.shortcuts import render
from django.views.generic import ListView , DetailView , CreateView , UpdateView , DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin , LoginRequiredMixin
from . models import Question , Comment
from . forms import CommentForm
from django.urls import reverse_lazy

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


class QuestionCreateView(LoginRequiredMixin , CreateView):
    model = Question
    template_name = 'stackbase/question_form.html'
    fields = ['title' , 'description']

    success_url = '/questions/'


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class QuestionUpdateView(UserPassesTestMixin , LoginRequiredMixin ,  UpdateView):
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
        

class CommentDetailView(DetailView):
    model = Comment
    form_class = CommentForm
    template_name = 'stackbase/question_detail.html'
    context_object_name = 'question'

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)
    
    success_url = reverse_lazy('stackbase:question-detail')

class AddCommentView(LoginRequiredMixin , CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'stackbase/question-answer.html'

    def form_valid(self, form): # This is for to know the user who is commenting and the question on which he is commenting
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.object.question.get_absolute_url()