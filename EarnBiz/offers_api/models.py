from django.db import models
from decimal import Decimal
from wallets_api.models import Transaction
from account_api.models import UserEarnProfil

# Create your models here.
class BaseOffer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('completed', 'Complété'),
        ('rejected', 'Rejeté'),
        ('chargeback', 'Chargeback'),
    ]
    external_tx_id = models.CharField(max_length=300, unique=True)
    offer_id = models.CharField(max_length=200, blank=True, null=True)
    offer_name = models.CharField(max_length=300, blank=True, null=True)
    reward_usd = models.DecimalField(max_digits=10, decimal_places=4)
    user_reward = models.DecimalField(max_digits=10, decimal_places=4)
    admin_reward = models.DecimalField(max_digits=10, decimal_places=4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    postback_raw = models.JSONField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class LootablyOffer(BaseOffer):
    # Lootably
    user = models.ForeignKey(UserEarnProfil, on_delete=models.CASCADE, related_name='lootably_offers')
    transaction = models.OneToOneField(Transaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='lootably_offer')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[Lootably] {self.user.email} | {self.offer_name} | {self.user_reward} USD"

class CPXResearchOffer(BaseOffer):
    # Sondages completes via CPX Research
    user  = models.ForeignKey(UserEarnProfil, on_delete=models.CASCADE, related_name='cpx_offers')
    transaction = models.OneToOneField(Transaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='cpx_offer')
    
    # Champs specifiques CPX Research
    survey_id  = models.CharField(max_length=100, blank=True, null=True)
    survey_duration = models.IntegerField(blank=True, null=True)
    hash_value = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[CPX] {self.user.email} | {self.offer_name} | {self.user_reward} USD"

class AdGemOffer(BaseOffer):
    #Offres complétées via AdGem
    user = models.ForeignKey(UserEarnProfil, on_delete=models.CASCADE, related_name='adgem_offers')
    transaction = models.OneToOneField(Transaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='adgem_offer')
    
    # Champs spécifiques AdGem
    app_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='App ID AdGem')
    placement = models.CharField(max_length=100, blank=True, null=True, verbose_name='Placement AdGem')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[AdGem] {self.user.full_name} | {self.offer_name} | {self.user_reward} USD"


