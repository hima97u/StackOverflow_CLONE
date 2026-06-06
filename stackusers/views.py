from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request , f'Account Successfully created for {username} ! Log In now :)')
            return redirect('stackbase:home')
    else:
         form = UserRegistrationForm()

    return render(request , 'stackusers/register.html' , {'form' : form})


@login_required
def profile(request):
    return render(request , 'stackusers/profile.html')