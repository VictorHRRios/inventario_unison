from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Tu perfil se ha actualizado!')
            # return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)


@staff_member_required
def display_profile(request, user_id):
    u_form = User.objects.get(id=user_id)

    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=u_form.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'El perfil se ha actualizado!')
            return redirect('display_profile', user_id)
    else:
        p_form = ProfileUpdateForm(instance=u_form.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/display_profile.html', context)


@staff_member_required
def manage_users(request):
    if request.user.is_staff:
        non_staff_users = User.objects.filter(is_staff=False)
        return render(request, 'users/manage_users.html',
                      {'non_staff_users': non_staff_users})
    else:
        messages.error(request, 'No tienes acceso a esta pagina')
    return render(request, 'users/manage_users.html')


@staff_member_required
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['email']
            new_user.save()
            messages.success(request, f'Your account has been created! You can now log in')
            return redirect('manage_users')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@staff_member_required
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


@staff_member_required
def deactivate_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('manage_users')

@staff_member_required
def activate_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('manage_users')
