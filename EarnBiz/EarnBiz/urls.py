"""
URL configuration for EarnBiz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account', include('account_api.urls')),
    path('api/wallets', include('wallets_api.urls')),
    path('api/adsviews', include('adsviews_api.urls')),
    path('api/bonus', include('bonus_api.urls')),
    path('api/core', include('core_api.urls')),
    path('api/marketing', include('marketing_api.urls')),
    path('api/missions', include('missions_api.urls')),
    path('api/notifications', include('notifications_api.urls')),
    path('api/offers', include('offers_api.urls'))
]
