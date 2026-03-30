from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from .forms import RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('chat:dashboard')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created successfully. Welcome to the chat app!')
        return redirect('chat:dashboard')
    return render(request, 'users/register.html', {'form': form})
