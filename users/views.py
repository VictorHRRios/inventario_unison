from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    return render(request, 'users/profile.html')
