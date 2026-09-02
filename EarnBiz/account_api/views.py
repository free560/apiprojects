from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .models import UserEarnProfil, UserWallManager
from .serializers import (LoginSerializer, UserSerializer, RegisterSerializer, UserEarnProfilSerializer, UserWallManagerSerializer)

User = get_user_model()

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

# LOGIN: retourne le token
class LoginViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            # USERNAME_FIELD = "email" sur le modèle User, donc on passe
            # directement email à authenticate()
            user = authenticate(username=email, password=password)

            if not user:
                return error_response("Identifiants invalides.", status.HTTP_401_UNAUTHORIZED)

            token, _ = Token.objects.get_or_create(user=user)
            return success_response(
                data={"token": token.key, "role": user.role},
                message="Connexion réussie."
            )

        return error_response("Données invalides.", status.HTTP_400_BAD_REQUEST)

# REGISTER crée le User + son profil vide selon le rôle
class RegisterViewSet(viewsets.ViewSet):
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            if user.role == "user_earn":
                UserEarnProfil.objects.get_or_create(user=user)
            elif user.role == "wallmanager":
                UserWallManager.objects.get_or_create(user=user)

            token, _ = Token.objects.get_or_create(user=user)
            return success_response(
                data={"user": UserSerializer(user).data, "token": token.key},
                message="Inscription réussie.",
                status_code=status.HTTP_201_CREATED
            )
        return error_response(message=str(serializer.errors))

# UserViewSet: profile(token) GET user data
class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

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

    @action(detail=False, methods=["get"], url_path="profile")
    def profile(self, request):
        # Retourne les données de l'utilisateur connecté.
        serializer = UserSerializer(request.user)
        return success_response(data=serializer.data, message="Profil utilisateur.")

# UserEarnProfilViewSet
class UserEarnProfilViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = UserEarnProfil.objects.select_related("user").all()
        if not request.user.is_staff:
            queryset = queryset.filter(user=request.user)
        serializer = UserEarnProfilSerializer(queryset, many=True)
        return success_response(data=serializer.data, message="Liste des profils User_Earn.")

    def retrieve(self, request, pk=None):
        try:
            profil = UserEarnProfil.objects.get(pk=pk)
        except UserEarnProfil.DoesNotExist:
            return error_response("Profil introuvable.", status.HTTP_404_NOT_FOUND)
        serializer = UserEarnProfilSerializer(profil)
        return success_response(data=serializer.data)

    def update(self, request, pk=None):
        try:
            profil = UserEarnProfil.objects.get(pk=pk)
        except UserEarnProfil.DoesNotExist:
            return error_response("Profil introuvable.", status.HTTP_404_NOT_FOUND)

        if profil.user != request.user and not request.user.is_staff:
            return error_response("Action non autorisée.", status.HTTP_403_FORBIDDEN)

        serializer = UserEarnProfilSerializer(profil, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(data=serializer.data, message="Profil mis à jour.")
        return error_response(message=str(serializer.errors))

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        # Retourne (ou crée) le profil User_Earn de l'utilisateur connecté.
        profil, _ = UserEarnProfil.objects.get_or_create(user=request.user)
        serializer = UserEarnProfilSerializer(profil)
        return success_response(data=serializer.data, message="Mon profil User_Earn.")

# UserWallManagerViewSet
class UserWallManagerViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = UserWallManager.objects.select_related("user").all()
        if not request.user.is_staff:
            queryset = queryset.filter(user=request.user)
        serializer = UserWallManagerSerializer(queryset, many=True)
        return success_response(data=serializer.data, message="Liste des profils WallManager.")

    def retrieve(self, request, pk=None):
        try:
            profil = UserWallManager.objects.get(pk=pk)
        except UserWallManager.DoesNotExist:
            return error_response("Profil introuvable.", status.HTTP_404_NOT_FOUND)
        serializer = UserWallManagerSerializer(profil)
        return success_response(data=serializer.data)

    def update(self, request, pk=None):
        try:
            profil = UserWallManager.objects.get(pk=pk)
        except UserWallManager.DoesNotExist:
            return error_response("Profil introuvable.", status.HTTP_404_NOT_FOUND)

        if profil.user != request.user and not request.user.is_staff:
            return error_response("Action non autorisée.", status.HTTP_403_FORBIDDEN)

        serializer = UserWallManagerSerializer(profil, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(data=serializer.data, message="Profil mis à jour.")
        return error_response(message=str(serializer.errors))

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        # Retourne (ou crée) le profil WallManager de l'utilisateur connecté.
        profil, _ = UserWallManager.objects.get_or_create(user=request.user)
        serializer = UserWallManagerSerializer(profil)
        return success_response(data=serializer.data, message="Mon profil WallManager.")

