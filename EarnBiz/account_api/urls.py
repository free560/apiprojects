from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

from .views import (LoginViewSet, RegisterViewSet, UserViewSet, UserEarnProfilViewSet, UserWallManagerViewSet)

router = DefaultRouter()
router.register(r"auth/login", LoginViewSet, basename="login")
router.register(r"auth/register", RegisterViewSet, basename="register")
router.register(r"users", UserViewSet, basename="user")
router.register(r"earn-profiles", UserEarnProfilViewSet, basename="earn-profile")
router.register(r"wallmanager-profiles", UserWallManagerViewSet, basename="wallmanager-profile")

urlpatterns = [
    path("", include(router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Endpoints générés automatiquement par le router, entre autres :
#   POST   /auth/login/                     -> connexion (token)
#   POST   /auth/register/                  -> inscription
#   GET    /users/                          -> liste des utilisateurs
#   GET    /users/{id}/                     -> détail d'un utilisateur
#   GET    /users/profile/                  -> profil de l'utilisateur connecté
#   GET    /earn-profiles/                  -> liste des profils User_Earn
#   GET    /earn-profiles/{id}/             -> détail d'un profil User_Earn
#   PUT    /earn-profiles/{id}/             -> mise à jour d'un profil User_Earn
#   GET    /earn-profiles/me/               -> mon profil User_Earn
#   GET    /wallmanager-profiles/           -> liste des profils WallManager
#   GET    /wallmanager-profiles/{id}/      -> détail d'un profil WallManager
#   PUT    /wallmanager-profiles/{id}/      -> mise à jour d'un profil WallManager
#   GET    /wallmanager-profiles/me/        -> mon profil WallManager
