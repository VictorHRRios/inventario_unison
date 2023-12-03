from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Item, ShoppingCart, Report, Order, User
from .forms import ItemCreateForm, DateRangeForm, ItemAddForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json


@login_required
def home(request):
    items = Item.objects.all()
    categories = items.values_list('category', flat=True).distinct()

    selected_category = request.GET.get('category')

    if selected_category:
        items = items.filter(category=selected_category)

    items = items.order_by('name')

    items_per_page = 12

    paginator = Paginator(items, items_per_page)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'title': 'Order Item',
        'items': items,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'inventory/request_item.html', context)


@staff_member_required
def movement_info(request, movement_id):
    orders = Order.objects.filter(report_id=movement_id)
    total = 0
    for order in orders:
        total += order.price * order.quantity
    return render(request, 'inventory/movement_info.html', {'title': 'Movement Info', 'orders': orders, 'total': total})


@staff_member_required
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
            cash = cash + (unit_price * quantity)
        outlays.append([str(mov.date), float(cash), str(mov.id)])

    for mov in entrys_movements:
        cash = 0
        for order in Order.objects.filter(report_id=mov):
            unit_price = order.item.unit_price
            quantity = order.quantity
            cash = cash + (unit_price * quantity)
        entrys.append([str(mov.date), float(cash), str(mov.id)])

    movements = {
        'outlays': json.dumps(outlays),
        'entrys': json.dumps(entrys)
    }
    return render(request, 'stats/budget_stats.html', {'title': 'Budget Stats', 'form': form, 'movements': movements})


@staff_member_required
def product_stats(request):
    items = []
    all_items = Item.objects.all()
    for item in all_items:
        items.append([item.name, float(item.sku)])
    data = {
        'items' : json.dumps(items),
    }
    return render(request, 'stats/product_stats.html', {'title': 'Product Stats', 'data' : data})


@staff_member_required
def movements(request):
    # movements = Report.objects.all().order_by('-date')
    movements_input = Report.objects.filter(movement='entrada').order_by('-date')
    movements_output = Report.objects.filter(movement='salida').order_by('-date')
    return render(request, 'inventory/movements.html',
                  {'title': 'Stock Movements', 'movements_input': movements_input,
                   'movements_output': movements_output})


@login_required
def shopping_cart(request):
    cart_items = ShoppingCart.objects.filter(user=request.user)
    for cart_item in cart_items:
        if cart_item.quantity > cart_item.item.stock:
            cart_item.quantity = cart_item.item.stock
            cart_item.save()
            messages.warning(request, f'El stock del carrito ha sido modificado.')
        elif cart_item.quantity == 0:
            cart_item.delete()
            messages.warning(request, f'Un elemento del carrito ha sido eliminado por cambios en el stock.')
            return redirect('shopping_cart')
    return render(request, 'inventory/shopping_cart.html', {'title': 'Shopping Cart', 'cart_items': cart_items})


@login_required
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
        messages.warning(request, f'No hay suficientes artículos en almacén.')
        cart_item.quantity = cart_item.item.stock
        cart_item.save()
    return redirect('shopping_cart')


@login_required
def remove_item(request, item_id):
    user = request.user
    cart_item = ShoppingCart.objects.get(pk=item_id, user=user)
    cart_item.delete()
    return redirect('shopping_cart')


@staff_member_required
def manage_items(request):
    items = Item.objects.all()

    categories = items.values_list('category', flat=True).distinct()

    selected_category = request.GET.get('category')

    if selected_category:
        items = items.filter(category=selected_category)
    items = items.order_by('name')
    items_per_page = 12

    paginator = Paginator(items, items_per_page)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'title': 'Gestion de articulos',
        'items': items,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'inventory/manage_items.html', context)


@staff_member_required
def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return redirect('manage_items')


@staff_member_required
def create_item(request):
    if request.method == 'POST':
        form = ItemCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tu artículo ha sido creado')
            return redirect('manage_items')
    else:
        form = ItemCreateForm()
    return render(request, 'inventory/create_item.html', {'form': form})


@login_required
def display_item(request, item_id):
    form = Item.objects.get(id=item_id)
    return render(request, 'inventory/display_item.html', {'form': form})


@staff_member_required
def update_item(request, item_id):
    item = Item.objects.get(id=item_id)
    form = ItemCreateForm(request.POST, instance=item)
    if request.method == 'POST':
        form = ItemCreateForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tu artículo ha sido actualizado.')
            return redirect('manage_items')
    else:
        form = ItemCreateForm(instance=item)
    return render(request, 'inventory/update_item.html', {'form': form})


@login_required
def save_cart(request):
    cart_items = ShoppingCart.objects.filter(user=request.user)

    reason = request.POST.get('reason')
    report = Report.objects.create(
        movement='salida',
        user=request.user,
        reason=reason
    )
    for cart_item in cart_items:
        Order.objects.create(
            item=cart_item.item,
            quantity=cart_item.quantity,
            price=cart_item.item.unit_price,
            report=report
        )
        cart_item.item.stock -= cart_item.quantity
        cart_item.item.save()
    report.save()
    cart_items.delete()
    messages.success(request, f'Se ha generado un reporte de la transacción.')

    return redirect('shopping_cart')


@staff_member_required
def add_stock(request):
    items = Item.objects.all()

    categories = items.values_list('category', flat=True).distinct()

    form = ItemAddForm()

    selected_category = request.GET.get('category')

    if selected_category:
        items = items.filter(category=selected_category)
    items = items.order_by('name')
    temp_user, created = User.objects.get_or_create(
        username="ADMIN",
        is_staff=True
    )
    cart_items = ShoppingCart.objects.filter(user=temp_user.id)
    context = {
        'title': 'Order Item',
        'items': items,
        'cart_items': cart_items,
        'categories': categories,
        'selected_category': selected_category,
        'form': form
    }
    return render(request, 'inventory/add_stock.html', context)


@staff_member_required
def add_to_stock(request, item_id):
    item = Item.objects.get(id=item_id)
    form = ItemAddForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data['addition']
        temp_user = User.objects.get(username="ADMIN")
        cart_item, created = ShoppingCart.objects.get_or_create(
            item=item,
            user=temp_user,
            defaults={'quantity': int(quantity)}
        )
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()
        return redirect('add_stock')
    else:
        messages.warning(request, f'Hubo un error al agregar al carrito.')
    return redirect('add_stock')


@staff_member_required
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
        Order.objects.create(
            item=cart_item.item,
            quantity=cart_item.quantity,
            price=cart_item.item.unit_price,
            report=report
        )
        cart_item.item.stock += cart_item.quantity
        cart_item.item.save()
    report.save()
    cart_items.delete()
    messages.success(request, f'Se ha generado un reporte de la transacción.')
    return redirect('manage_items')


@staff_member_required
def remove_item_stock(request, item_id):
    temp_user = User.objects.get(username="ADMIN")
    cart_item = ShoppingCart.objects.get(pk=item_id, user=temp_user)
    cart_item.delete()
    return redirect('add_stock')
