from django.db import models
from decimal import Decimal
# Create your models here.

# PARAMÈTRES SYSTÈME (singleton)
class SystemSettings(models.Model):
    # Répartition
    admin_share_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('60.00'), verbose_name='% Admin')
    user_share_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('40.00'), verbose_name='% Utilisateur')

    # Retraits
    min_withdrawal_amount = models.DecimalField(max_digits=8,  decimal_places=2, default=Decimal('1.00'))
    max_withdrawal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('500.00'))

    # Frais
    crypto_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('1.00'),  verbose_name='Frais')
    mobile_money_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('2.00'))
    local_system_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))

    # Parrainage
    referral_bonus_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('5.00'))

    #   Lootably
    lootably_api_key = models.CharField(max_length=200, blank=True)
    lootably_postback_secret = models.CharField(max_length=200, blank=True)
    lootably_enabled = models.BooleanField(default=True)

    # CPX Research 
    cpx_app_id = models.CharField(max_length=100, blank=True)
    cpx_secure_hash_secret = models.CharField(max_length=300, blank=True)
    cpx_postback_secret = models.CharField(max_length=200, blank=True)
    cpx_enabled = models.BooleanField(default=True)

    # AdGem
    adgem_app_id = models.CharField(max_length=100, blank=True)
    adgem_api_key  = models.CharField(max_length=200, blank=True)
    adgem_postback_secret = models.CharField(max_length=200, blank=True)
    adgem_enabled = models.BooleanField(default=True)

    # Système
    maintenance_mode = models.BooleanField(default=False)
    site_name        = models.CharField(max_length=100, default='RewardPlatform')
    site_currency    = models.CharField(max_length=10,  default='USD')
    updated_at       = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Paramètres — Admin {self.admin_share_percentage}% / User {self.user_share_percentage}%"

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
