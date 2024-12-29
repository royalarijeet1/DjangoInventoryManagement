from django import forms
from .models import Product,Assembly,Component


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['customer']


class AssemblyForm(forms.ModelForm):
    class Meta:
        model = Assembly
        fields=['name']


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        exclude=['assembly']



