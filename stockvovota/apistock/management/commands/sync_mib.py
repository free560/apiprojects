from django.core.management.base import BaseCommand
from votre_app.services import MIBService

class Command(BaseCommand):
    help = 'Synchronise les produits depuis l\'API MadeInBurundi'

    def handle(self, *args, **kwargs):
        self.stdout.write("Synchronisation en cours...")
        if MIBService.sync_products():
            self.stdout.write(self.style.SUCCESS("Produits synchronisés avec succès !"))
        else:
            self.stdout.write(self.style.ERROR("Échec de la synchronisation."))