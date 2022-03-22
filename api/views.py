from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from .serializers import CategoriesSerializer, ManufacturersSerializer, ProductsSerializer, OrdersSerializer,\
    UsersSerializer
from .models import Categories, Manufacturers, Products, Orders, Users


class APICategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class APIManufacturersViewSet(viewsets.ModelViewSet):
    queryset = Manufacturers.objects.all()
    serializer_class = ManufacturersSerializer


class APIProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class APIOrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


class APIUsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if not username or not password:
            raise exceptions.AuthenticationFailed('No credentials provided.')

        user = authenticate(username=username, password=password)

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid username/password.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        if not user.is_staff:
            raise exceptions.AuthenticationFailed('User is not a staff')

        try:
            return Response({'token': Token.objects.get(user=user).key})
        except Exception as e:
            Token.objects.create(user=user)
            return Response({"token": user.auth_token.key})
