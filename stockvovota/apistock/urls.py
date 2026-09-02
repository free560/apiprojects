from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from .views import *

router = DefaultRouter()
router.register(r'login', LoginViewSet, basename='login')
router.register(r'history', HistoryViewSet, basename='history')
router.register(r'stocks', StockViewSet, basename='stock')
router.register(r'users', UserViewSet, basename='user')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'stock-in', StockInViewSet, basename='stock-in')
router.register(r'stock-out', StockOutViewSet, basename='stock-out')
router.register(r'productinstock', ProductInStockViewSet, basename='productinstock')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]