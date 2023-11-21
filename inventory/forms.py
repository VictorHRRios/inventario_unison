from django import forms
from .models import Item, ShoppingCart


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'image', 'category', 'description', 'unit_type', 'unit_price', 'stock', 'low_stock_threshold',
                  'unison']


class QuantityForm(forms.ModelForm):
    CHOICES = [(i, str(i)) for i in range(1, 11)]
    quantity = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = ShoppingCart
        fields = ['quantity']
