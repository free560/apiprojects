from django.db import models
from decimal import Decimal
from account_api.models import UserEarnProfil

# Create your models here.
class AdView(models.Model):
    AD_TYPE_CHOICES = [
        ('banner','Bannière'),('video','Vidéo'),
        ('interstitial','Interstitielle'),('rewarded','Pub Récompensée'),
    ]

    user = models.ForeignKey(UserEarnProfil, on_delete=models.CASCADE, related_name='ad_views')
    ad_type  = models.CharField(max_length=20, choices=AD_TYPE_CHOICES)
    ad_network = models.CharField(max_length=50, default='adsense')
    revenue = models.DecimalField(max_digits=8, decimal_places=6, default=Decimal('0.000000'))
    user_share = models.DecimalField(max_digits=8, decimal_places=6, default=Decimal('0.000000'))
    admin_share = models.DecimalField(max_digits=8, decimal_places=6, default=Decimal('0.000000'))
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.user.full_name} | {self.ad_type} | +{self.user_share} USD"

    def save(self, *args, **kwargs):
        if self.revenue:
            self.user_share  = self.revenue * Decimal('0.60')
            self.admin_share = self.revenue * Decimal('0.40')
        super().save(*args, **kwargs)
