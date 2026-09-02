from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserEarnProfil, UserWallManager

User = get_user_model()


# LOGIN
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


# USER (compte de base)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "created_at"]
        read_only_fields = ["id", "created_at"]


class RegisterSerializer(serializers.ModelSerializer):
    # Inscription commune. Le champ `role` détermine si un profil
    # UserEarnProfil ou UserWallManager sera créé côté vue.
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "password", "password2", "role"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        if attrs["role"] not in dict(User.ROLE_CHOICES):
            raise serializers.ValidationError({"role": "Rôle invalide."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password = validated_data.pop("password"),
            role=validated_data.get('role'),
        )
        return user

# PROFIL USER_EARN
class UserEarnProfilSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)

    class Meta:
        model = UserEarnProfil
        fields = [
            "id", "user", "email", "role", "pro_avatar", "phone", "full_name",
            "gender", "country", "city", "date_of_barth",
            "is_verified", "is_banned", "ip_adress",
            "refferal_code", "reffered_by",
            "created_at", "update_at",
        ]
        read_only_fields = [
            "id", "user", "email", "role", "is_verified", "is_banned",
            "refferal_code", "created_at", "update_at",
        ]


# PROFIL WALLMANAGER
class UserWallManagerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)

    class Meta:
        model = UserWallManager
        fields = [
            "id", "user", "email", "role", "pro_avatar", "phone", "full_name",
            "gender", "country", "city", "date_of_barth",
            "is_verified", "is_block",
            "created_at", "update_at",
        ]
        read_only_fields = ["id", "user", "email", "role", "is_verified", "is_block", "created_at", "update_at"]
