from django import forms
from .models import Item, ShoppingCart


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'image', 'category', 'description', 'unit_type', 'unit_price', 'low_stock_threshold',
                  'unison']


class TextForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 2}),
                             label='Especifíca porqué necesitas estos objetos.')
