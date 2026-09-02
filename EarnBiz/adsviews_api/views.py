from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .models import AdView
from .serializers import AdViewSerializer
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


class AdViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    
