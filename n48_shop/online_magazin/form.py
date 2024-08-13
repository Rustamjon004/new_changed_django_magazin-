
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



class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=255)

    class Meta:
        model = user
        fields = ('username', 'email', 'password')

    def clean_username(self):
        username = self.data.get('username')
        if user.objects.filter(username=username).exists():
            raise forms.ValidationError(f'This {username} is already exists')
        return username

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data['password']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True

        if commit:
            user.save()

        return user

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
