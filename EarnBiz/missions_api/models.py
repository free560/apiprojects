from django.db import models
from account_api.models import UserEarnProfil

# Create your models here.
class Mission(models.Model):
    MISSION_TYPE = [
        ('offers', 'Compléter des offres'),
        ('ads', 'Regarder des publicités'),
        ('earn', 'Gagner un montant'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    mission_type = models.CharField(max_length=20, choices=MISSION_TYPE)
    target_value = models.IntegerField(help_text="Ex: 5 offres ou 10 ads")
    reward = models.DecimalField(max_digits=10, decimal_places=4)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.reward})"
        
        
        
class UserMission(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'En cours'),
        ('completed', 'Complété'),
        ('claimed', 'Réclamé'),
    ]

    user = models.ForeignKey(UserEarnProfil, on_delete=models.CASCADE, related_name='missions')
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    completed_at = models.DateTimeField(blank=True, null=True)
    claimed_at   = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'mission')

    def __str__(self):
        return f"{self.user.username} | {self.mission.title} | {self.progress}/{self.mission.target_value}"
        
     