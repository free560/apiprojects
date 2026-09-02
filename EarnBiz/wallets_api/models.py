from django.db import models
from account_api.models import UserEarnProfil
from decimal import Decimal

# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(UserEarnProfil, on_delete=models.CASCADE, related_name='wallet')
    balence =  models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_earned = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_withdrawn = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_referral_bonus = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    earned_lootably = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    earned_cpx = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    earned_rewardsOffer= models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    earned_ads = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    is_frozon = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"wallet of {self.user.user.email}({self.user.user.role})"

class AdminWallet(models.Model):
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    revenue_lootably = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    revenue_cpx = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    revenue_rewardsoffer = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    revenue_ads = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    updated = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return f"Admin total Wallets {self.total_revenue}"

class Transaction(models.Model):

    TYPE_CHOICES = [
        ('lootably',   'Offerwall Lootably'),
        ('cpx',        'Offerwall CPX Research'),
        ('adgem',      'Offerwall rewardsoffer'),
        ('ads',        'Publicité (Ads)'),
        ('referral',   'Bonus Parrainage'),
        ('bonus',      'Bonus Admin'),
        ('withdrawal', 'Retrait'),
        ('refund',     'Remboursement'),
    ]
    STATUS_CHOICES = [
        ('pending',   'En attente'),
        ('completed', 'Complété'),
        ('failed',    'Échoué'),
        ('reversed',  'Annulé'),
    ]

    user = models.ForeignKey(UserEarnProfil, on_delete = models.CASCADE, related_name='tran_user')
    type_tran = models.CharField(max_length=15, choices=TYPE_CHOICES)
    status_tran = models.CharField(max_length=30, choices=STATUS_CHOICES)
    gross_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    user_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    admin_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), blank=True)
    external_transaction_id = models.CharField(max_length=10, blank=True, null=True)
    offer_name = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    note_tran = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    
    def save(self, *args, **kwargs):
        if self.gross_amount and not self.user_amount:
            self.user_amount  = (self.gross_amount * Decimal('0.40')).quantize(Decimal('0.0001'))
            self.admin_amount = (self.gross_amount * Decimal('0.60')).quantize(Decimal('0.0001'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaction of {self.user.full_name}"


class WithdrawalRequest(models.Model):
    METHOD_CHOICES = [
        ('crypto_btc',   'Bitcoin (BTC)'),
        ('crypto_usdt',  'USDT (TRC20/ERC20)'),
    ]
    STATUS_CHOICES = [
        ('pending',    'En attente'),
        ('processing', 'En cours'),
        ('completed',  'Payé'),
        ('rejected',   'Rejeté'),
        ('cancelled',  'Annulé'),
    ]
    CRYPTO_NETWORK_CHOICES = [
        ('trc20',   'TRC20 (Tron)'),
        ('erc20',   'ERC20 (Ethereum)'),
        ('bep20',   'BEP20 (BSC)'),
        ('bitcoin', 'Bitcoin'),
    ]

    user = models.ForeignKey(UserEarnProfil, on_delete=models.CASCADE, related_name="user_withdrawalRequest")
    method = models.CharField(max_length=100, choices=METHOD_CHOICES)
    status =  models.CharField(max_length=100, choices=STATUS_CHOICES)
    amount_requested = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    fee = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    crypto_address = models.CharField(max_length=300, blank=True, null=True)
    crypto_network = models.CharField(max_length=100, choices=CRYPTO_NETWORK_CHOICES, blank=True, null=True)
    crypto_tx_hash = models.CharField(max_length=300, blank=True, null=True)

    mobile_number   = models.CharField(max_length=20, blank=True, null=True)
    mobile_provider = models.CharField(max_length=50, blank=True, null=True)
    mobile_name     = models.CharField(max_length=100, blank=True, null=True)
    mobile_tx_id    = models.CharField(max_length=200, blank=True, null=True)

    local_account_id   = models.CharField(max_length=100, blank=True, null=True)
    local_account_name = models.CharField(max_length=100, blank=True, null=True)
    local_tx_reference = models.CharField(max_length=200, blank=True, null=True)


    admin_note   = models.TextField(blank=True, null=True)
    processed_by = models.ForeignKey(UserEarnProfil, on_delete=models.SET_NULL, null=True, blank=True,related_name='processed_withdrawals')
    processed_at = models.DateTimeField(blank=True, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name} | {self.method} | {self.amount_requested} | {self.status}"

    def approve(self, processed_by_user):
        self.status = 'completed'
        self.processed_by = processed_by_user
        self.processed_at = timezone.now()
        self.amount_paid = self.amount_requested - self.fee
        self.save()

    def reject(self, processed_by_user, reason=''):
        self.status = 'rejected'
        self.processed_by = processed_by_user
        self.processed_at = timezone.now()
        self.admin_note = reason
        self.user.wallet.credit(self.amount_requested)
        self.save()


    
