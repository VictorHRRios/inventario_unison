from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='inventory-home'),
    path('about/', views.about, name='inventory-about'),
    path('reports/', views.reports, name='reports-reports'),
    path('reports/budget/', views.budget_report, name='reports-budget-report'),
    path('reports/product/', views.product_report, name='reports-product-report'),
    path('stock_movements/', views.stock_movements, name='inventory-stock_movements'),
    
    
]
