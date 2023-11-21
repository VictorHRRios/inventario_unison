from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Item, ShoppingCart
from .forms import ItemCreateForm, QuantityForm


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
    cart_items = ShoppingCart.objects.filter(user=request.user)
    return render(request, 'inventory/shopping_cart.html', {'title': 'Shopping Cart', 'cart_items': cart_items})


def order_item(request):
    item = Item.objects.all()
    if request.method == 'POST':
        # form = QuantityForm(request.POST)
        # if form.is_valid():
        # form = form.cleaned_data['quantity']
        context = {
            'title': 'Order Item',
            'item': item,
            # 'form': form
        }
        return render(request, 'inventory/order_item.html', context)
    else:
        # form = QuantityForm()
        context = {
            'title': 'Order Item',
            'item': item,
            # 'form': form
        }
    return render(request, 'inventory/order_item.html', context)


def add_to_cart(request, item_id):
    item = Item.objects.get(id=item_id)
    cart_item, created = ShoppingCart.objects.get_or_create(
        item=item,
        user=request.user,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    cart_item.item.stock -= 1
    cart_item.item.save()
    return redirect('order_item')


def remove_item(request, item_id):
    user = request.user
    cart_item = ShoppingCart.objects.get(pk=item_id, user=user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    cart_item.item.stock += 1
    cart_item.item.save()
    return redirect('shopping_cart')


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
            messages.success(request, f'Tu articulo ha sido agregado al carrito')
            return redirect('manage_items')
    else:
        form = ItemCreateForm()
    return render(request, 'inventory/create_item.html', {'form': form})


def display_item(request, item_id):
    form = Item.objects.get(id=item_id)
    return render(request, 'inventory/display_item.html', {'form': form})


def update_item(request, item_id):
    item = Item.objects.get(id=item_id)
    form = ItemCreateForm(request.POST, instance=item)
    if request.method == 'POST':
        form = ItemCreateForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tu articulo ha sido actualizado')
            return redirect('manage_items')
    else:
        form = ItemCreateForm(instance=item)
    return render(request, 'inventory/update_item.html', {'form': form})
