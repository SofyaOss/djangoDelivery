from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Restaurant, Product, ProductInBasket


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        # fields = ['id', 'restaurant_name', 'restaurant_rating', 'rest_image']
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = ['id', 'restaurant_name', 'restaurant_rating', 'rest_image']
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PasswordSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['confirm_password'] != attrs['new_password']:
            raise ValidationError('incorrect password')

    class Meta:
        model = User
        fields = '__all__'


class ProdInBasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInBasket
        fields = '__all__'
