from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from .models import *
from .serializers import *



# Helper response builder
def success_response(data=None, message="", status_code=status.HTTP_200_OK):
    return Response({
        "success": True,
        "message": message,
        "data": data
    }, status=status_code)


def error_response(message="", status_code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "success": False,
        "message": message,
        "data": None
    }, status=status_code)


# Token login → retourne le token

class LoginViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            # Note: On passe souvent email à 'username' sauf si tu as configuré 
            # spécifiquement ton modèle User pour accepter email=email
            user = authenticate(username=email, password=password)
            
            if not user:
                return error_response("Identifiants invalides.", status.HTTP_401_UNAUTHORIZED)

            token, _ = Token.objects.get_or_create(user=user)
            return success_response(
                data={"token": token.key},
                message="Connexion réussie."
            )
        
        # Si le serializer n'est pas valide (ex: email mal formé)
        return error_response("Données invalides.", status.HTTP_400_BAD_REQUEST)

# StockViewSet
class StockViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = Stock.objects.all()
        serializer = StockSerializer(queryset, many=True)
        return success_response(data=serializer.data)

    def retrieve(self, request, pk=None):
        try:
            stock = Stock.objects.get(pk=pk)
        except Stock.DoesNotExist:
            return error_response("Stock introuvable.", status.HTTP_404_NOT_FOUND)
        serializer = StockSerializer(stock)
        return success_response(data=serializer.data)

    def create(self, request):
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(data=serializer.data, message="Stock créé.", status_code=status.HTTP_201_CREATED)
        return error_response(message=str(serializer.errors))

    def update(self, request, pk=None):
        try:
            stock = Stock.objects.get(pk=pk)
        except Stock.DoesNotExist:
            return error_response("Stock introuvable.", status.HTTP_404_NOT_FOUND)
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(data=serializer.data, message="Stock mis à jour.")
        return error_response(message=str(serializer.errors))

    def destroy(self, request, pk=None):
        try:
            stock = Stock.objects.get(pk=pk)
        except Stock.DoesNotExist:
            return error_response("Stock introuvable.", status.HTTP_404_NOT_FOUND)
        stock.delete()
        return success_response(message="Stock supprimé.")


# UserViewSet  →  profile(token) GET user data
class UserViewSet(viewsets.ViewSet):
    #permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return success_response(data=serializer.data)

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return error_response("Utilisateur introuvable.", status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return success_response(data=serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(data=serializer.data, message="Utilisateur créé.", status_code=status.HTTP_201_CREATED)
        return error_response(message=str(serializer.errors))

    @action(detail=False, methods=["get"], url_path="profile")
    def profile(self, request):
        #Retourne les données de l'utilisateur connecté.
        serializer = UserSerializer(request.user)
        return success_response(data=serializer.data, message="Profil utilisateur.")

# ProductViewSet  →  product(token) GET product list
class ProductViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        #Retourne la liste de tous les produits.
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return success_response(data=serializer.data, message="Liste des produits.")

    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return error_response("Produit introuvable.", status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return success_response(data=serializer.data)


# StockInViewSet  →  stockin(token) POST + history
class StockInViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        #etourne l'historique des entrées en stock.
        queryset = StockIn.objects.all().order_by("-created_at")
        serializer = StockInSerializer(queryset, many=True)
        return success_response(data=serializer.data, message="Historique des entrées en stock.")

    def create(self, request):
        #POST /api/stockin/
        serializer = StockInSerializer(data=request.data)
        if serializer.is_valid():
            stock_in = serializer.save(user=request.user)
            return success_response(
                data={
                    "code": stock_in.code,
                    "created_at": stock_in.created_at,
                },
                message="Entrée en stock enregistrée.",
                status_code=status.HTTP_201_CREATED
            )
        return error_response(message=str(serializer.errors))

    def retrieve(self, request, pk=None):
        try:
            stock_in = StockIn.objects.get(pk=pk)
        except StockIn.DoesNotExist:
            return error_response("Entrée introuvable.", status.HTTP_404_NOT_FOUND)
        serializer = StockInSerializer(stock_in)
        return success_response(data=serializer.data)


# StockOutViewSet: stockout POST + getstockout GET
class StockOutViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        #Retourne la liste des sorties { product_id, number }.
        
        queryset = StockOut.objects.all().order_by("-created_at")

        product_id = request.query_params.get("product_id")
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        serializer = StockOutSerializer(queryset, many=True)
        return success_response(data=serializer.data, message="Liste des sorties en stock.")

    def create(self, request):
    
        serializer = StockOutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return success_response(
                message="Sortie de stock enregistrée avec succès.",
                status_code=status.HTTP_201_CREATED
            )
        return error_response(message=str(serializer.errors))

    def retrieve(self, request, pk=None):
        try:
            stock_out = StockOut.objects.get(pk=pk)
        except StockOut.DoesNotExist:
            return error_response("Sortie introuvable.", status.HTTP_404_NOT_FOUND)
        serializer = StockOutSerializer(stock_out)
        return success_response(data=serializer.data)


# ProductInStockViewSet: productinstock + search
class ProductInStockViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        #Retourne la liste des produits en stock pour un stock donné.
        queryset = ProductInStock.objects.all()

        stock_id = request.query_params.get("stock_id")
        if stock_id:
            queryset = queryset.filter(stock_id=stock_id)

        serializer = ProductInStockSerializer(queryset, many=True)
        return success_response(data=serializer.data, message="Produits en stock.")

    def retrieve(self, request, pk=None):
        try:
            pis = ProductInStock.objects.get(pk=pk)
        except ProductInStock.DoesNotExist:
            return error_response("Produit en stock introuvable.", status.HTTP_404_NOT_FOUND)
        serializer = ProductInStockSerializer(pis)
        return success_response(data=serializer.data)

    @action(detail=False, methods=["get"], url_path="search")
    def search_product(self, request):

        #Recherche un produit dans le stock par nom ou code.
        query = request.query_params.get("q", "").strip()
        if not query:
            return error_response("Paramètre de recherche 'q' requis.")

        queryset = ProductInStock.objects.filter(
            product__name__icontains=query
        ) | ProductInStock.objects.filter(
            product__code__icontains=query
        )

        serializer = ProductInStockSerializer(queryset.distinct(), many=True)
        return success_response(data=serializer.data, message=f"Résultats pour '{query}'.")


# HistoryViewSet  →  History(token) GET stock_in + stock_out
class HistoryViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        
        #Retourne l'historique combiné des entrées et sorties en stock.        
        stock_ins  = StockIn.objects.all().order_by("-created_at")
        stock_outs = StockOut.objects.all().order_by("-created_at")

        stock_in_serializer  = StockInSerializer(stock_ins, many=True)
        stock_out_serializer = StockOutSerializer(stock_outs, many=True)

        return success_response(
            data={
                "stock_in":  stock_in_serializer.data,
                "stock_out": stock_out_serializer.data,
            },
            message="Historique des mouvements de stock."
        )