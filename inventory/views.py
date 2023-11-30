from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Item, ShoppingCart, Report, Order
from .forms import ItemCreateForm, DateRangeForm
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
    form = DateRangeForm()
    outlays = []
    entrys = []
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
    
    outlays_movements = Report.objects.filter(movement='salida')
    entrys_movements = Report.objects.filter(movement='entrada')
    
    for mov in outlays_movements:
        cash = 0
        for order in Order.objects.filter(report_id=mov):
            unit_price = order.item.unit_price
            quantity = order.quantity
            cash = cash + (unit_price*quantity)
        outlays.append([str(mov.date), float(cash)])

    for mov in entrys_movements:
        cash = 0
        for order in Order.objects.filter(report_id=mov):
            unit_price = order.item.unit_price
            quantity = order.quantity
            cash = cash + (unit_price*quantity)
        entrys.append([str(mov.date.year), float(cash)])

    movements = {
        'outlays' : json.dumps(outlays),
        'entrys' : json.dumps(entrys)
    }

    #movements['outlays_mov'] = json.dumps(movements['outlays'])
    return render(request, 'stats/budget_stats.html', {'title': 'Budget Stats', 'form' : form, 'movements' : movements})


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
