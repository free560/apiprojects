from django.db import models
from account_api.models import UserEarnProfil

# Create your models here.
class Notification(models.Model):
    TYPE_CHOICES = [
        ('earning','Gain reçu'),('withdrawal','Retrait'),
        ('referral','Parrainage'),('system','Système'),('bonus','Bonus'),
    ]

    user = models.ForeignKey(UserEarnProfil, on_delete=models.CASCADE, related_name='notifications')
    type_not = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} | {self.title} | {'Lu' if self.is_read else 'Non lu'}"

