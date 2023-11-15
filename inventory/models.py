from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

"""
Comandos para cada actualizacion de los modelos
python manage.py makemigrations
python manage.py migrate
"""

class Report(models.Model):
    TYPE_MOVEMENT = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

    date = models.DateField(default=timezone.now)
    movement = models.CharField(max_length=10, choices=TYPE_MOVEMENT) #input or output
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    items = models.JSONField(default=list, blank=True) # List of two things: (Reference to the article (foreignKey) . amount)

    def __str__(self):
        return f"[{self.date}] {self.user.username} : {self.movement}"

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('papeleria', 'Papelería'),
        ('limpieza', 'Limpieza'),
        ('plomeria', 'Plomería'),
        ('electricidad', 'Electricidad'),
    ]

    UNIT_CHOICES = [
        ('paquete', 'Paquete'),
        ('block', 'Block'),
        ('individual', 'Individual'),
        ('caja', 'Caja'),
    ]

    name = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    unit_type = models.CharField(max_length=20, choices=UNIT_CHOICES)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=10)
    unison = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.id}] {self.category} : {self.stock}"

