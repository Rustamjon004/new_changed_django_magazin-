
from django import forms
from .models import Comment, Product
from .models import Order
from .models import Product
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['full_name', 'product', 'text']





class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'status']


class OrderModelForm(forms.ModelForm):
    class Mate:
        model = Order
        exclude = ['product']

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'