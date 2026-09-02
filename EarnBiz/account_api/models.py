from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [('user_earn', 'User_Earn'), ('wallmanager', 'WallManager')]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length = 30, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.email} ({self.role})"


class UserEarnProfil(models.Model):
    GENDER_CHOICES = [('male', 'Homme'),('female', 'Femme'),('other','Autre')]

    user = models.OneToOneField('User', on_delete=models.CASCADE)
    pro_avatar = models.ImageField(upload_to='profil_image')
    phone = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=30, blank=True, null= True)
    gender = models.CharField(max_length=10, blank=True, choices=GENDER_CHOICES)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    date_of_barth = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    ip_adress = models.GenericIPAddressField(blank=True, null=True)
    refferal_code = models.CharField(max_length=15, unique=True, blank=True, null=True)
    reffered_by = models.ForeignKey('self',on_delete = models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.refferal_code:
            self.refferal_code = str(uuid.uuid4()).replace('-', '').upper()[:10]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Profile of {self.user.email} ({self.user.role})"

class UserWallManager(models.Model):
    GENDER_CHOICES = [('male', 'Homme'),('female', 'Femme'),('other','Autre')]

    user = models.OneToOneField('User', on_delete=models.CASCADE)
    pro_avatar = models.ImageField(upload_to='profil_image')
    phone = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=30, blank=True, null= True)
    gender = models.CharField(max_length=10, blank=True, choices=GENDER_CHOICES)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    date_of_barth = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.email} ({self.user.role})"
