from django.contrib.auth.models import User

from rest_framework import serializers

from .models import *


class CategoriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categories
        fields = ('__all__')


class ManufacturersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Manufacturers
        fields = ('__all__')


class ProductsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Products
        fields = ('__all__')


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ('url', 'username', 'email', 'is_staff')


class OrdersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Orders
        fields = ('__all__')