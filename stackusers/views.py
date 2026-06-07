from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import UserRegistrationForm  , UserUpdateForm , ProfileUpdateForm
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


def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST , instance=request.user)
        p_form = ProfileUpdateForm(request.POST , request.FILES , instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request , f'Your account has been updated successfully !')
            return redirect('profile')
    
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        'u_form' : u_form , 
        'p_form' : p_form
    }

    return render(request , 'stackusers/profile_update.html' , context)
