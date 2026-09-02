from django.db import models
from account_api.models import UserWallManager, UserEarnProfil
from decimal import Decimal

# Create your models here.
class Wall(models.Model):
    user = models.ForeignKey(UserWallManager, on_delete=models.CASCADE)
    mallname = models.CharField(max_length=100, blank=True, null=True)
    adress = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mall of {self.user.full_name} in {self.user.address}"

class Product(models.Model):
    mall = models.ForeignKey(Wall, on_delete=models.CASCADE)
    creator = models.ForeignKey(UserWallManager, on_delete=models.CASCADE)
    name_product = models.CharField(max_length=150)
    imageproduct = models.ImageField(upload_to='productImage')
    description = models.TextField()
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    tranport_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    stock_quantite = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product of {self.mall.mallname}";

class Order(models.Model):
    agent_marketing = models.ForeignKey(UserEarnProfil, on_delete=models.SET_NULL, null=True)
    wallmanager = models.ForeignKey(UserWallManager, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order creater by {self.wallmanager.full_name} order mission of {self.agent_marketing.full_name}";

class Commission(models.Model):
    agent_marketing = models.ForeignKey(UserEarnProfil, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    profit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    commission_rate = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(str):
        return f"commison of {self.agent_marketing.full_name},commission_amount({self.commission_amount})"
