
from django.db import models
# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:  # Bu joyda bo'sh joy to'g'ri bo'lishi kerak
        abstract = True

class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.title

class Product(BaseModel):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='products', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value)
    discount = models.PositiveIntegerField(default=0)

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    def __str__(self) -> str:
        return self.name

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.username

class Comment(BaseModel):
    full_name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    def __str__(self):
        return self.text

class Order(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('sending', 'Sending'),
        ('fast delivered', 'Fast Delivered'),
        ('be canceled', 'Be Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')

    def __str__(self):
        return self.status


class Order(BaseModel):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    quanity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f'{self.name} -{self.phone}'
