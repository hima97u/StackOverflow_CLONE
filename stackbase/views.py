from django.shortcuts import render , get_object_or_404 
from django.http import HttpResponseRedirect
from django.urls import reverse
from . models import Question , Comment
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

def like_view(request , pk):
    post = get_object_or_404(Question , id=request.POST.get('question_id'))
    liked  = False

    if post.likes.filter(id=request.user.id).exists(): # if the user has already liked the post then remove the like otherwise add the like
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('stackbase:question-detail' , args=[str(pk)]))

class QuestionListView(ListView):
    model = Question
    template_name = 'stackbase/question_list.html'
    context_object_name = 'questions'
    ordering = ['-created_at']
    
    
class QuestionDetailView(DetailView):
    model = Question
    template_name = 'stackbase/question_detail.html'
    context_object_name = 'question'

    # this is for to show the total likes of a question in the question detail page
    def get_context_data(self, *args , **kwargs):
        context = super(QuestionDetailView , self).get_context_data(*args , **kwargs)
        question = get_object_or_404(Question , id=self.kwargs['pk'])

        # # debugging
        # print("User:", self.request.user)
        # print("User ID:", self.request.user.id)
        # print("Likes:", list(question.likes.all()))
        # print("Liked:", question.likes.filter(id=self.request.user.id).exists())


        total_likes = question.total_likes()
        liked = False
        if question.likes.filter(id=self.request.user.id).exists(): # if the user has already liked the post then show the liked button otherwise show the like button
            liked = True
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context





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