from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='inventory-home'),
    path('manage_items/', views.manage_items, name='manage_items'),
    path('delete_item/<int:item_id>/', views.delete_item, name="delete_item"),
    path('display_item/<int:item_id>/', views.display_item, name="display_item"),
    path('create_item/', views.create_item, name='create_item'),
    path('reports/', views.reports, name='reports-reports'),
    path('reports/budget/', views.budget_report, name='reports-budget-report'),
    path('reports/product/', views.product_report, name='reports-product-report'),
    path('stock_movements/', views.stock_movements, name='inventory-stock_movements'),
    path('shopping_cart/', views.shopping_cart, name='inventory-shopping_cart'),

]
