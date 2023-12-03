from django import forms
from .models import Item, ShoppingCart


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'image', 'sku', 'category', 'description', 'unit_type', 'unit_price', 'low_stock_threshold',
                  'unison']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Nombre'
        self.fields['image'].label = 'Imagen'
        self.fields['category'].label = 'Categoria'
        self.fields['description'].label = 'Descripcion'
        self.fields['unit_type'].label = 'Tipo de Unidad'
        self.fields['unit_price'].label = 'Precio de Unidad'
        self.fields['low_stock_threshold'].label = 'Umbral de existencias'


class TextForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 2}),
                             label='Especifíca porqué necesitas estos objetos.')


class ItemAddForm(forms.Form):
    addition = forms.IntegerField(label='Cantidad a agregar', widget=forms.NumberInput(attrs={'type': 'number'}))

    def clean_addition(self):
        addition = self.cleaned_data.get('addition')

        if addition is not None and addition <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor que 0.')

        return addition


class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Fecha inicio', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='Fecha final', widget=forms.DateInput(attrs={'type': 'date'}))
