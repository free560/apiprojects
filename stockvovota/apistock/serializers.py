from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'},trim_whitespace=False, required=True)

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'name', 'location', 'created_at']



class UserSerializer(serializers.ModelSerializer):
    stock_name = serializers.CharField(source='stock.name', read_only=True)
    stock_location = serializers.CharField(source='stock.location', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 
            'phone', 'stock', 'stock_name', 'stock_location', 'password'
        ]
        #Securite
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ''),
            phone=validated_data.get('phone', ''),
            stock=validated_data.get('stock')
        )
        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class StockInSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    stock_name = serializers.CharField(source='stock.name', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = StockIn
        fields = [
            'id', 'user', 'user_name', 'stock', 'stock_name', 'product', 
            'product_details', 'number', 'expire_date', 'truck_number', 
            'code', 'created_at'
        ]
        read_only_fields = ['code', 'user', 'created_at']

class StockOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockOut
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

    def validate(self, data):
        if data['number'] > data['stock_in'].number:
            raise serializers.ValidationError(
                {"number": "La quantité de sortie ne peut pas dépasser la quantité d'entrée initiale."}
            )
        return data


class ProductInStockSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    stock_name = serializers.CharField(source='stock.name', read_only=True)

    class Meta:
        model = ProductInStock
        fields = ['id', 'product', 'product_name', 'stock', 'stock_name', 'number', 'created_at']