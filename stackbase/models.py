
from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    likes = models.ManyToManyField(User, related_name='question_posts')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.title}'


    def get_absolute_url(self):
     return reverse('stackbase:question-detail', kwargs={'pk': self.pk})
    
    # function for counting the total likes of a question
    def total_likes(self):
        return self.likes.count()
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    name = models.TextField(max_length=20)
    body = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - Comment on {self.question.title}'

    def get_absolute_url(self):
        return reverse('stackbase:question-detail', kwargs={'pk': self.question.pk})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.question.save()  # Update the question's timestamp when an answer is saved