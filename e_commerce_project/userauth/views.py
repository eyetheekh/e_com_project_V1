from django.shortcuts import redirect, render
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            user = authenticate(
                request=request, username=username, password=password)
            if user:
                login(request=request, user=user)
            messages.success(request, 'Registration Success! Happy Shopping.')
            return redirect('core:home')
        else:
            messages.error(request, 'Registration Failed, Try Again!')
    form = RegisterForm()
    return render(request, 'userauth/register.html', {
        'form': form,
    })


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request=request, username=username, password=password)
        if user:
            login(request=request, user=user)
            messages.success(request, 'Login Success, Enjoy Shopping!')
            return redirect('core:home')
        else:
            messages.error(request, 'Login Failed, Try Again!')

    return render(request, 'userauth/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged Out!')
    return redirect('core:home')
