
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['full_name', 'product', 'text']



from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'status']
