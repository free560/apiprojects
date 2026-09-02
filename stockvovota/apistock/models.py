from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
import string

class Stock(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

from django.db import models

class Product(models.Model):
    external_id = models.IntegerField(unique=True, help_text="ID provenant de l'API MadeInBurundi")
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (MIB-{self.external_id})"

def generate_stock_code():
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(10))

class StockIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # ID venant de madeinBURUNDI
    number = models.PositiveIntegerField()
    expire_date = models.DateField()
    truck_number = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"product stock in user {self.stock.name}"

class StockOut(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    stock_in = models.ForeignKey(StockIn, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    truck_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product out in Stock {self.stock.name}"

class ProductInStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"product in Stock {self.stock.name}"
