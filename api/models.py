from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

from .managers import UsersManager


class Users(AbstractUser):
    STATUS_CHOICE = [
        ('ONLINE', 'Онлайн'),
        ('OFFLINE', 'Оффлайн'),
        ('DELETE', 'Удалён'),
        ('BLOCKED', 'Заблокирован'),
    ]
    email = models.EmailField(max_length=127, blank=False, null=False, unique=True, verbose_name='Электронная почта')
    username = models.CharField(max_length=127, blank=False, null=False, unique=True, verbose_name='Имя пользователя')
    ip_address = models.CharField(max_length=255, blank=True, null=False, default='', verbose_name='IP-адрес',
                                  help_text='Для ограничения доступа пользователя на сайт')
    status = models.CharField(max_length=16, blank=False, null=False, verbose_name='Статус', choices=STATUS_CHOICE,
                              default='OFFLINE')
    discount = models.IntegerField(blank=False, null=False, default='0')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UsersManager()

    class Meta:
        ordering = ["username"]
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Categories(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, null=False, default='', verbose_name='Описание',
                                   help_text='Содержит краткое описание товаров, которые можно найти в данной рубрике.')
    availability = models.BooleanField(blank=True, null=False, default=False, verbose_name='Доступность',
                                       help_text='Доступность категории при просмотре. в случае отсутствия - в '
                                                 'категории нет товаров')
    quantity_of_goods = models.IntegerField(blank=True, null=False, default=0, verbose_name='Количество товаров',
                                            editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Manufacturers(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True, verbose_name='Наименование')
    description = models.TextField(blank=True, null=False, default='', verbose_name='Описание',
                                   help_text='Содержит краткое описание производителя: историю фирмы, сертификаты '
                                             'качества, различные награды и участие в выставках, повышающие доверие '
                                             'покупателей.')
    quantity_of_goods = models.IntegerField(blank=True, null=False, default=0, verbose_name='Количество товаров',
                                            editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"


class Products(models.Model):
    # Потом будет смысл тянуть на главную страницу самые популярные товары
    name = models.CharField(max_length=255, blank=False, null=False, unique=True, verbose_name='Наименование')
    description = models.JSONField(blank=True, null=True, verbose_name='Описание',
                                   help_text='Описание продукта в формате JSON '
                                             '{"blocks":[{"header":"","description":""}]}')
    price = models.IntegerField(blank=True, null=False, default='0', verbose_name='Цена')
    availability = models.BooleanField(blank=True, null=False, default=True, verbose_name='Доступность')
    option = models.JSONField(blank=True, null=True, verbose_name='Опции',
                              help_text='Список различных характеристик в формате JSON '
                                        '{"blocks":["blockname":"",{"options":[{"name":"","value":""}]}]}')
    product_categories = models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, to=Categories,
                                           verbose_name='Категория')
    product_manufacturers = models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, to=Manufacturers,
                                              verbose_name='Производитель')
    quantity_of_goods = models.IntegerField(blank=True, null=False, default=0, verbose_name='Количество товаров',
                                            editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Images(models.Model):
    images = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Изображение')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return str(self.images)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class Slider(models.Model):
    # Тут могут быть акции, реклама каких-то новых товаров, целых брендов и т.д.
    name = models.CharField(max_length=128, blank=False, null=False, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, null=False, default='', verbose_name='Описание',
                                   help_text='Содержит краткое описание товаров, которые можно найти в данной рубрике.')
    products = models.ManyToManyField(Products)
    path = models.CharField(max_length=256, blank=False, null=False, unique=True, verbose_name='Путь',
                            help_text='Путь отностительно главной страницы по которому будет представлен данный объект')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Слайдер"
        verbose_name_plural = "Слайдер"


class Orders(models.Model):
    DELIVERY_METHOD = [
        ('DELIVERY', 'Доставка'),
        ('PICKUP', 'Самовывоз'),
    ]
    PAYMENT_METHOD = [
        ('CASH', 'Наличные'),
        ('BANKCARD', 'Банковская карта'),
    ]
    STATUS = [
        ('ASSEMBLED', 'Собирается клиентом'),
        ('INPROCESSING', 'В обработке'),
        ('COMPLETED', 'Выполнен'),
        ('REJECTED', 'Отклонен'),
    ]
    customers = models.ForeignKey(Users, blank=False, null=False, on_delete=models.CASCADE,
                                  verbose_name='Пользователь')
    order_price = models.IntegerField(blank=False, null=False, default='0', verbose_name='Цена заказа')
    quantity_of_goods = models.IntegerField(blank=False, null=False, default=0, verbose_name='Количество товаров')
    delivery_method = models.CharField(max_length=16, blank=False, null=False, verbose_name='Способ доставки',
                                       choices=DELIVERY_METHOD, default='OFFLINE')
    payment_method = models.CharField(max_length=16, blank=False, null=False, verbose_name='Способ доставки',
                                      choices=PAYMENT_METHOD, default='CASH')
    status = models.CharField(max_length=16, blank=False, null=False, verbose_name='Способ доставки',
                              choices=STATUS, default='ASSEMBLED')
    commentary = models.TextField(blank=True, null=False, default='')

    def __str__(self):
        return f"id{self.id}"

    class Meta:
        ordering = ["customers"]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Basket(models.Model):
    product = models.ForeignKey(Products, verbose_name='Товар', on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, verbose_name='Заказ', on_delete=models.CASCADE)
    count = models.IntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return str(self.product_id)

    class Meta:
        ordering = ["id"]
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
