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

def reports(request):
    return render(request, 'reports/reports.html', {'title' : 'Reports'})

def reports(request):
    return render(request, 'reports/reports.html', {'title' : 'Reports'})

def budget_report(request):
    return render(request, 'reports/budget_report.html', {'title' : 'Budget Report'})

def product_report(request):
    return render(request, 'reports/product_report.html', {'title' : 'Product Report'})


def stock_movements(request):
    return render(request, 'inventory/stock_movements.html', {'title' : 'Stock Movements'})

def shopping_cart(request):
    return render(request, 'inventory/shopping_cart.html', {'title' : 'Shopping Cart'})