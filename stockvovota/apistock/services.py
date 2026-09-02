import requests
from django.conf import settings
from .models import Product

class MIBService:
    @staticmethod
    def get_token():
        try:
            response = requests.post(settings.MIB_TOKEN_URL, json={
                "email": settings.MIB_EMAIL,
                "password": settings.MIB_PASSWORD
            }, timeout=10) # Ajout d'un timeout pour eviter que l'API ne bloque ton site
            
            response.raise_for_status() 
            return response.json().get("access")
        except Exception as e:
            print(f"Erreur de connexion (Token) : {e}")
            return None

    @classmethod
    def sync_products(cls):
        token = cls.get_token()
        if not token:
            return False
            
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = requests.get(settings.MIB_API_URL, headers=headers, timeout=15)
            if response.status_code == 200:
                products = response.json()
                
                # Utilisation d'une transaction pour plus de rapidité (Optionnel mais Pro)
                from django.db import transaction
                with transaction.atomic():
                    for item in products:
                        Product.objects.update_or_create(
                            external_id=item['id'],
                            defaults={'name': item.get('name', 'Produit sans nom')}
                        )
                return True
        except Exception as e:
            print(f"Erreur de synchronisation : {e}")
            
        return False