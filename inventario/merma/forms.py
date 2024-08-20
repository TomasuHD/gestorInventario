from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, ItemInventario, Proveedor
from datetime import date

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1',  'password2']

class ItemInventarioForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0, label='Categoría')
    provider = forms.ModelChoiceField(queryset=Proveedor.objects.all(), initial=0, label='Proveedor')
    entry_date = forms.DateField(
        initial=date.today, 
        label='Fecha de Entrada',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = ItemInventario
        fields = ['name', 'quantity', 'category', 'provider', 'entry_date']
        labels = {
            'name': 'Nombre',
            'quantity': 'Cantidad',
            'category': 'Categoría',
            'provider': 'Proveedor',
            'entry_date': 'Fecha de Entrada'
        }

    def clean_entry_date(self):
        entry_date = self.cleaned_data.get('entry_date')
        if entry_date > date.today():
            raise forms.ValidationError("La fecha de entrada no puede ser futura.")
        return entry_date