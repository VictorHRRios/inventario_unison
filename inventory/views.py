from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    context = {

    }
    return render(request, 'inventory/home.html', context)

def about(request):
    return render(request, 'inventory/about.html', {'title': 'About'})

def reports(request):
    return render(request, 'reports/reports.html', {'title' : 'Reports'})
