from django.db.models.signals import post_save
from django.dispatch import receiver

from wallets_api.models import Wallet, AdminWallet
from .models import User, UserEarnProfil, UserWallManager


@receiver(post_save, sender=User)
def create_user_profile_and_wallets(sender, instance, created, **kwargs):

    print("hello signals")

    if created:

        # SUPERUSER
        if instance.is_superuser or instance.is_staff:

            print("signals superuser create success")

            AdminWallet.objects.get_or_create(user=instance)

        # USER EARN
        elif instance.role == "user_earn":

            print("signals create user_earn")

            # Create profile
            profile, created_profile = UserEarnProfil.objects.get_or_create(user=instance)

            # Create wallet linked to UserEarnProfil
            Wallet.objects.get_or_create(user=profile)

        # WALL MANAGER
        elif instance.role == "wallmanager":

            print("signals wallmanager create success")

            UserWallManager.objects.get_or_create(user=instance)