from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Item
from .forms import ItemCreateForm


@login_required
def home(request):
    context = {

    }
    return render(request, 'inventory/home.html', context)


def reports(request):
    return render(request, 'reports/reports.html', {'title': 'Reports'})


def budget_report(request):
    return render(request, 'reports/budget_report.html', {'title': 'Budget Report'})


def product_report(request):
    return render(request, 'reports/product_report.html', {'title': 'Product Report'})


def stock_movements(request):
    return render(request, 'inventory/stock_movements.html', {'title': 'Stock Movements'})


def shopping_cart(request):
    return render(request, 'inventory/shopping_cart.html', {'title': 'Shopping Cart'})


def manage_items(request):
    items = Item.objects.all()
    return render(request, 'inventory/manage_items.html', {'items': items})


def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return redirect('manage_items')


def create_item(request):
    if request.method == 'POST':
        form = ItemCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tu articulo ha sido creado')
            return redirect('manage_items')
    else:
        form = ItemCreateForm()
    return render(request, 'inventory/create_item.html', {'form': form})


def display_item(request, item_id):
    form = Item.objects.get(id=item_id)
    return render(request, 'inventory/display_item.html', {'form': form})
