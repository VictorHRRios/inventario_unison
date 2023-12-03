from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

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

    date = models.DateTimeField(default=timezone.now)
    movement = models.CharField(max_length=10, choices=TYPE_MOVEMENT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"[{self.id}] {self.user.username} : {self.movement}"


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
    image = models.ImageField(default='default_item.jpg', upload_to='item_pics')
    sku = models.DecimalField(max_digits=10, decimal_places=0, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    unit_type = models.CharField(max_length=20, choices=UNIT_CHOICES)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=10)
    unison = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.name}] {self.category} : {self.stock}"

    def save(self):
        super().save()
        with Image.open(self.image.path) as img:
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)


class Order(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.report}] {self.item.name} : {self.quantity}"


class ShoppingCart(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Shopping Cart"
