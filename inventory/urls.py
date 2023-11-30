from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='inventory-home'),
    path('manage_items/', views.manage_items, name='manage_items'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('delete_item/<int:item_id>/', views.delete_item, name="delete_item"),
    path('display_item/<int:item_id>/', views.display_item, name="display_item"),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name="add_to_cart"),
    path('add_to_stock/<int:item_id>/', views.add_to_stock, name="add_to_stock"),
    path('remove_item/<int:item_id>/', views.remove_item, name="remove_item"),
    path('remove_item_stock/<int:item_id>/', views.remove_item_stock, name="remove_item_stock"),
    path('create_item/', views.create_item, name='create_item'),
    path('update_item/<int:item_id>/', views.update_item, name='update_item'),
    path('movements/movement_info/<int:movement_id>/', views.movement_info, name='movement_info'),
    path('stats/budget/', views.budget_stats, name='budget_stats'),
    path('stats/product/', views.product_stats, name='product_stats'),
    path('movements', views.movements, name='movements'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('save_cart/', views.save_cart, name='save_cart'),
    path('save_input/', views.save_input, name='save_input'),
    path('request_item/', views.request_item, name='request_item'),
]
