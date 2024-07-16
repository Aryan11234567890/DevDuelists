from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
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
    search_query = request.GET.get('search') if request.GET.get('search') else ''
    problems = Problem.objects.filter(
        Q(name__icontains=search_query)
    )
    return render(request, 'problems.html', {'problems': problems, 'search_query': search_query})

@login_required(login_url = 'login')
def discussionPage(request):
    return render(request, 'Discussions.html')

@login_required(login_url = 'login')
def solvePage(request, id):
    problem = get_object_or_404(Problem, id=id)
    return render(request, 'solve.html', {'problem': problem})

@login_required(login_url = 'login')
def logoutButton(request):
    logout(request)
    return redirect('login')