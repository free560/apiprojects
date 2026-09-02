from django.db import models
from account_api.models import UserEarnProfil

# Create your models here.
class Bonus(models.Model):
    BONUS_TYPE = [
        ('welcome', 'Bonus inscription'),
        ('daily', 'Bonus journalier'),
        ('activity', 'Bonus activité'),
    ]

    title = models.CharField(max_length=200)
    bonus_type = models.CharField(max_length=20, choices=BONUS_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=4)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.amount} USD)"   
        
            
class UserBonus(models.Model):
    user  = models.ForeignKey(UserEarnProfil, on_delete=models.CASCADE, related_name='bonuses')
    bonus = models.ForeignKey(Bonus, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.bonus.title} | {self.amount} USD"    
