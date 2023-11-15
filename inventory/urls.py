from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='inventory-home'),
    path('about/', views.about, name='inventory-about'),
    path('reports/', views.reports, name='reports-reports'),
    path('stock_movements/', views.stock_movements, name='inventory-stock_movements')
    #path('reports/budget', views.budget_report, name='inventory-budget-report'),
    #path('reports/product', views.product_report, name='inventory-product-report'),
    
]
