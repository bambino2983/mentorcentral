from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from  .models import Kb, Category
from .forms import KbForm



def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User not exist')

        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
             messages.error(request, 'Username or Password no existe')
    context= {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    kbs = Kb.objects.filter(
        Q(category__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
    )

    topics = Category.objects.all()
    kb_count = kbs.count()
    context = {'kbs': kbs, 'topics': topics, 'kb_count': kb_count}
    return render(request, 'base/home.html', context)


def kb(request, pk):
    kb = Kb.objects.get (id=pk)  
    kb_messages = kb.message_set.all()
    context = {'kb': kb, 'kb_messages': messages}
    return render(request, 'base/kb.html', context)

@login_required(login_url='login')
def createKb(request):
    form = KbForm()
    if request.method == "POST":
        form = KbForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/kb_form.html', context)

@login_required(login_url='login')
def updateKb(request, pk):
    kb = Kb.objects.get (id=pk)   
    form = KbForm(instance=kb)

    if request.user != kb.creator:
        return HttpResponse('No estas autorizado')

    if request.method == "POST":
        form = KbForm(request.POST, instance=kb)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/kb_form.html', context)

def deleteKb(request, pk):
    kb = Kb.objects.get (id=pk) 

    if request.user != kb.creator:
        return HttpResponse('No estas autorizado')   
        
    if request.method == "POST":
        kb.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':kb})