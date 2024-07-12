
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
            
        except:
            messages.error(request, 'Player DNE...')
        
        user = authenticate(request, username = username, password = password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
    
    context = {}
    return render(request, 'login.html', context)

@login_required(login_url = 'login')
def homePage(request):
    context = {}
    
    return render(request, 'home.html', context)