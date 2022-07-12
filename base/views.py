from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from  .models import Kb, Category, Message, User
from .forms import KbForm, UserForm



def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')
            
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
    kb_messages = Message.objects.filter(Q(kb__category__name__icontains=q))

    context = {'kbs': kbs, 'topics': topics,
                'kb_count': kb_count, 'kb_messages': kb_messages}
    return render(request, 'base/home.html', context)


def kb(request, pk):
    kb = Kb.objects.get(id=pk)  
    kb_messages = kb.message_set.all().order_by('-created')
    partners = kb.partners.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            kb=kb,
            description=request.POST.get('description')
        )
        kb.partners.add(request.user)
        return redirect('kb', pk=kb.id)

    context = {'kb': kb, 'kb_messages': kb_messages,
                'partners': partners}
    return render(request, 'base/kb.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    kbs = user.kb_set.all()
    kb_messages = user.message_set.all()
    category = Category.objects.all()
    context = {'user': user, 'kbs': kbs, 'kb_messages':kb_messages, 'category':category}
    return render(request, 'base/profile.html', context)



@login_required(login_url='login')
def createKb(request):
    form = KbForm() 
    categories = Category.objects.all()
    if request.method == "POST":
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)

        Kb.objects.create(
            creator=request.user,
            category=category,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    
    context = {'form': form, 'categories': categories}
    return render(request, 'base/kb_form.html', context)

@login_required(login_url='login')
def updateKb(request, pk):
    kb = Kb.objects.get (id=pk)   
    form = KbForm(instance=kb)
    categories = Category.objects.all()
    if request.user != kb.creator:
        return HttpResponse('No estas autorizado')

    if request.method == "POST":
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)
        kb.name = request.POST.get('name')
        kb.category = category
        kb.description = request.POST.get('description')
        kb.save()
        return redirect('home')

    context = {'form': form, 'categories': categories, 'kb': kb}
    return render(request, 'base/kb_form.html', context)

@login_required(login_url='login')
def deleteKb(request, pk):
    kb = Kb.objects.get (id=pk) 

    if request.user != kb.creator:
        return HttpResponse('No estas autorizado')   
        
    if request.method == "POST":
        kb.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':kb})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get (id=pk) 

    if request.user != message.user:
        return HttpResponse('No estas autorizado')   
        
    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})
