from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth import logout
from .models import Post, Image, UserProfile
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'home.html')


def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        user_creator = request.user
        post = Post.objects.create(
            title=title,
            description=description,
            user_creator=user_creator
        )
        post.save()
        return redirect('home')
    return render(request, 'post_create.html')


def search_users(request):
    search_name = request.GET.get('search_name', '').strip()

    if search_name:
        users = User.objects.filter(
            Q(username__icontains=search_name) |
            Q(email__icontains=search_name)
        )
    else:
        users = []

    context = {
        'search_name': search_name,
        'users': users,
    }

    return render(request, 'search_users.html', context)


@login_required
def my_profile(request):
    return render(request, 'my_profile.html')
