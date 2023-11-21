from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='inventory-home'),
    path('manage_items/', views.manage_items, name='manage_items'),
    path('delete_item/<int:item_id>/', views.delete_item, name="delete_item"),
    path('display_item/<int:item_id>/', views.display_item, name="display_item"),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name="add_to_cart"),
    path('remove_item/<int:item_id>/', views.remove_item, name="remove_item"),
    path('create_item/', views.create_item, name='create_item'),
    path('update_item/<int:item_id>', views.update_item, name='update_item'),
    path('reports/', views.reports, name='reports'),
    path('reports/budget/', views.budget_report, name='budget_report'),
    path('reports/product/', views.product_report, name='product-report'),
    path('stock_movements/', views.stock_movements, name='stock_movements'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('order_item/', views.order_item, name='order_item'),

]
