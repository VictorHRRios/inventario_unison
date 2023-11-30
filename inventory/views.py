from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Item, ShoppingCart, Report, Order, User
from .forms import ItemCreateForm, ItemAddForm, DateRangeForm
import json


@login_required
def home(request):
    context = {
    }
    return render(request, 'inventory/home.html', context)


def movement_info(request, movement_id):
    orders = Order.objects.filter(report_id=movement_id)
    print(orders.all())
    return render(request, 'inventory/movement_info.html', {'title': 'Movement Info', 'orders': orders})


def budget_stats(request):
    return render(request, 'stats/budget_stats.html', {'title': 'Budget Stats'})


def product_stats(request):
    return render(request, 'stats/product_stats.html', {'title': 'Product Stats'})


def movements(request):
    movements = Report.objects.all()
    return render(request, 'inventory/movements.html',
                  {'title': 'Stock Movements', 'movements': movements})


def shopping_cart(request):
    cart_items = ShoppingCart.objects.filter(user=request.user)
    for cart_item in cart_items:
        if cart_item.quantity > cart_item.item.stock:
            cart_item.quantity = cart_item.item.stock
            cart_item.save()
            messages.warning(request, f'El stock del carrito ha sido modificado')
        elif cart_item.quantity == 0:
            cart_item.delete()
            messages.warning(request, f'Un elemento del carrito ha sido eliminado por cambios en el stock')
            return redirect('shopping_cart')
    return render(request, 'inventory/shopping_cart.html', {'title': 'Shopping Cart', 'cart_items': cart_items})


def request_item(request):
    item = Item.objects.all()
    context = {
        'title': 'Order Item',
        'item': item,
    }
    return render(request, 'inventory/request_item.html', context)


def add_to_cart(request, item_id):
    item = Item.objects.get(id=item_id)
    quantity = request.POST.get('quantity')
    cart_item, created = ShoppingCart.objects.get_or_create(
        item=item,
        user=request.user,
        defaults={'quantity': int(quantity)}
    )
    if not created:
        cart_item.quantity += int(quantity)
        cart_item.save()
    if cart_item.quantity > cart_item.item.stock:
        messages.warning(request, f'No hay suficientes articulos en el carrito')
        cart_item.quantity = cart_item.item.stock
        cart_item.save()
    return redirect('request_item')


def remove_item(request, item_id):
    user = request.user
    cart_item = ShoppingCart.objects.get(pk=item_id, user=user)
    cart_item.delete()
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
            messages.success(request, f'Tu articulo ha sido creado')
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


def save_cart(request):
    cart_items = ShoppingCart.objects.filter(user=request.user)

    reason = request.POST.get('reason')
    report = Report.objects.create(
        movement='salida',
        user=request.user,
        reason=reason
    )
    for cart_item in cart_items:
        order = Order.objects.create(
            item=cart_item.item,
            quantity=cart_item.quantity,
            report=report
        )
        cart_item.item.stock -= cart_item.quantity
        cart_item.item.save()
    report.save()
    order.save()
    cart_items.delete()

    return redirect('shopping_cart')


def add_stock(request):
    item = Item.objects.all()
    temp_user = User.objects.get(username="ADMIN")
    cart_items = ShoppingCart.objects.filter(user=temp_user.id)
    context = {
        'title': 'Order Item',
        'item': item,
        'cart_items': cart_items
    }
    return render(request, 'inventory/add_stock.html', context)


def add_to_stock(request, item_id):
    item = Item.objects.get(id=item_id)
    quantity = request.POST.get('quantity')
    username = "ADMIN"
    temp_user, created = User.objects.get_or_create(
        username=username,
    )
    cart_item, created = ShoppingCart.objects.get_or_create(
        item=item,
        user=temp_user,
        defaults={'quantity': int(quantity)}
    )
    if not created:
        cart_item.quantity += int(quantity)
        cart_item.save()
        print(cart_item.quantity)
    return redirect('add_stock')


def save_input(request):
    temp_user = User.objects.get(username="ADMIN")
    cart_items = ShoppingCart.objects.filter(user=temp_user.id)
    reason = request.POST.get('reason')
    report = Report.objects.create(
        movement='entrada',
        user=temp_user,
        reason=reason
    )
    for cart_item in cart_items:
        order = Order.objects.create(
            item=cart_item.item,
            quantity=cart_item.quantity,
            report=report
        )
        cart_item.item.stock += cart_item.quantity
        cart_item.item.save()
    report.save()
    order.save()
    cart_items.delete()
    return redirect('manage_items')
