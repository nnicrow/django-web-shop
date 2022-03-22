from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, get_user_model
from django.core.paginator import Paginator

from rest_framework.authtoken.models import Token
from ariadne import ObjectType, gql, make_executable_schema, load_schema_from_path, MutationType

from api.models import Categories, Manufacturers, Products, Images, Slider, Users, Orders, Basket


def paginate(quryset):
    return Paginator(quryset, 25)


class QueryResolver:
    query = ObjectType("Query")

    @staticmethod
    @query.field('categories')
    def resolve_categories(obj, info, id=None, page=1):
        return paginate(Categories.objects.all() if not id
                        else Categories.objects.filter(id=id)).page(page)

    @staticmethod
    @query.field('manufacturers')
    def resolve_manufacturers(obj, info, id=None, page=1):
        return paginate(Manufacturers.objects.all() if not id
                        else Manufacturers.objects.filter(id=id)).page(page)

    @staticmethod
    @query.field('products')
    def resolve_products(obj, info, id=None, page=1):
        return paginate(Products.objects.filter(availability=True) if not id
                        else Products.objects.filter(id=id, availability=True)).page(page)

    @staticmethod
    @query.field('user')
    def resolve_user(obj, info, token):
        return Users.objects.get(auth_token=token)

    @staticmethod
    @query.field('images')
    def resolve_images(obj, info, page=1):
        return paginate(Images.objects.all()).page(page)

    @staticmethod
    @query.field('slider')
    def resolve_slider(*_):
        return Slider.objects.all()

    @staticmethod
    @query.field('isAuthenticated')
    def resolve_auth(obj, info, token):
        return Token.objects.filter(key=token).exists()


class CategoriesResolver:
    categories = ObjectType("Categories")

    @staticmethod
    @categories.field('products')
    def resolve_categories(obj, info, page=1):
        return paginate(Products.objects.filter(product_categories=obj)).page(page)

    @staticmethod
    @categories.field('images')
    def resolve_categories(obj, info, page=1):
        return paginate(Images.objects.filter(content_type=ContentType.objects.get_for_model(Categories),
                                              object_id=obj.id)).page(page)


class ManufacturersResolver:
    manufacturers = ObjectType("Manufacturers")

    @staticmethod
    @manufacturers.field('products')
    def resolve_manufacturers(obj, info, page=1):
        return paginate(Products.objects.filter(product_manufacturers=obj)).page(page)

    @staticmethod
    @manufacturers.field('images')
    def resolve_manufacturers(obj, info, page=1):
        return paginate(Images.objects.filter(content_type=ContentType.objects.get_for_model(Manufacturers),
                                              object_id=obj.id)).page(page)


class ProductsResolver:
    products = ObjectType("Products")

    @staticmethod
    @products.field('images')
    def resolve_products(obj, info, page=1):
        return paginate(Images.objects.filter(content_type=ContentType.objects.get_for_model(Products),
                                              object_id=obj.id)).page(page)


class SliderResolver:
    slider = ObjectType("Slider")

    @staticmethod
    @slider.field('images')
    def resolve_slider(obj, info):
        return Images.objects.filter(content_type=ContentType.objects.get_for_model(Slider), object_id=obj.id)


class MutationResolver:
    mutation = MutationType()

    @staticmethod
    @mutation.field('login')
    def resolve_login(_, info, username: str, password: str) -> dict:
        if not username or not password:
            return {'status': False, 'token': None, 'err': 'Данные не предоставленны'}

        user = authenticate(username=username, password=password)
        if user is None:
            return {'status': False, 'token': None, 'err': 'Неправильные логин или пароль'}

        if not user.is_active:
            return {'status': False, 'token': None, 'err': 'Пользователь заморожен или удалён'}

        try:
            return {'status': True, 'token': Token.objects.get(user=user).key, 'err': None}
        except:
            Token.objects.create(user=user)
            return {'status': True, 'token': user.auth_token.key, 'err': None}

    @mutation.field('registration')
    def resolve_registration(_, info, username: str, password: str, email: str, first_name: str = '',
                             last_name: str = ''):
        if not email or not username or not password:
            return {'status': False, 'token': None, 'err': 'Данные не предоставленны'}

        if Users.objects.filter(email=email).exists():
            return {'status': False, 'token': None, 'err': 'Этот адрес электронной почту уже используется'}

        if Users.objects.filter(username=username).exists():
            return {'status': False, 'token': None, 'err': 'Это имя пользователя уже занято'}

        if len(password) < 8:
            return {'status': False, 'token': None, 'err': 'Пароль слишком короткий'}

        user = Users.objects.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        Token.objects.create(user=user)
        return {'status': True, 'token': user.auth_token.key, 'err': None}

    @staticmethod
    @mutation.field('orders')
    def resolve_orders(_, info, token: str, *args, **kwargs):
        id = kwargs.get('id', None)
        if id:
            user = Users.objects.get(auth_token=token)
            order = Orders.objects.get(customers=user, status='ASSEMBLED')
            order.status = 'INPROCESSING'
            order.save()
            Orders(customers=user).save()
        return Orders.objects.get(customers=Users.objects.get(auth_token=token), status='ASSEMBLED')

    @staticmethod
    @mutation.field('basket')
    def resolve_basket(_, info, token: str, *args, **kwargs):
        id = kwargs.get('id', None)
        product = kwargs.get('product', None)
        count = kwargs.get('count', None)
        order = Orders.objects.get(customers=Users.objects.get(auth_token=token), status='ASSEMBLED')
        if id:
            if count > 0:
                q = Basket.objects.get(id=id)
                basket_q = Basket.objects.get(id=id)
                product_q = Products.objects.filter(id=basket_q.product.id)[0]
                old_price = basket_q.count * product_q.price
                q.count = count
                q.save()
                order_q = Orders.objects.get(id=order.id, status='ASSEMBLED')
                basket_q = Basket.objects.get(id=id)
                product_q = Products.objects.get(id=basket_q.product.id)
                order_q.order_price += basket_q.count * product_q.price - old_price
                order_q.save()
            elif count == -1:
                order_q = Orders.objects.get(id=order.id, status='ASSEMBLED')
                basket_q = Basket.objects.get(id=id)
                product_q = Products.objects.get(id=basket_q.product.id)
                order_q.order_price -= basket_q.count * product_q.price
                order_q.save()
                Basket.objects.get(id=id).delete()
        elif product:
            if not Basket.objects.get(order=order, product=product):
                product_q = Products.objects.get(id=product)
                Basket(product=product_q, order=order).save()
                order_q = Orders.objects.get(id=order.id, status='ASSEMBLED')
                order_q.order_price += product_q.price
                order_q.save()
        return Basket.objects.filter(order=order)


class BasketResolver:
    basket = ObjectType("Basket")

    @staticmethod
    @basket.field('product')
    def resolve_product(obj, info):
        return obj.product

    @staticmethod
    @basket.field('order')
    def resolve_order(obj, info):
        return obj.order
