from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Problem

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
    
    context = {}
    return render(request, 'login.html', context)

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Oops! Something went wrong. Please try again.')
    
    return render(request, 'register.html', {'form': form})

@login_required(login_url='login')
def homePage(request):
    context = {}
    return render(request, 'home.html', context)

@login_required(login_url = 'login')
def problemPage(request):
    problems = Problem.objects.all()
    return render(request, 'problems.html', {'problems': problems})

@login_required(login_url = 'login')
def discussionPage(request):
    return render(request, 'Discussions.html')
