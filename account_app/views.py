from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import customUserCreationForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login , logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) 
            return redirect('tasks_list')
    else:
        form = AuthenticationForm()

    return render(request, 'account_app/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = customUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = customUserCreationForm()
    return render(request, 'account_app/registration.html', {'form': form})