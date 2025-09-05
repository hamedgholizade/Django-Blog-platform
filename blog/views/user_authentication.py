from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from blog.forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import permission_required
from blog.models import User


def user_registration(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return render(request, 'registration/register.html', {"form": form})
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return render(request, 'registration/register.html', {"form": form})

            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('user_login')
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'registration/register.html', {"form": form})
        
    form = RegistrationForm()
    return render(request, 'registration/register.html', {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')
