from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='inventory-home'),
    path('about/', views.about, name='inventory-about'),
]
