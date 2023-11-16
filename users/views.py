from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm


@login_required
def profile(request):
    return render(request, 'users/profile.html')


def manage_users(request):
    if request.user.is_staff:
        staff_users = User.objects.filter(is_staff=True)
        non_staff_users = User.objects.filter(is_staff=False)
        return render(request, 'users/manage_users.html',
                      {'staff_users': staff_users, 'non_staff_users': non_staff_users})
    else:
        messages.error(request, 'No tienes acceso a esta pagina')
    return render(request, 'users/manage_users.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can now log in')
            return redirect('manage_users')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def update_user(request, user_id):
    user = User.objects.get(id=user_id)
    form = UserUpdateForm(request.POST, instance=user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'La informacion del ususario se ha actualizado.')
            return redirect('manage_users')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'users/update_user.html', {'form': form})


def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('manage_users')
