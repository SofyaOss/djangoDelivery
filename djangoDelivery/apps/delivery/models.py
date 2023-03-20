from django.db import models
from django.db.models.signals import post_save
from simple_history.models import HistoricalRecords


class Restaurant(models.Model):
    restaurant_name = models.CharField('Название ресторана', max_length=200, blank=True, null=True, default=None)
    restaurant_rating = models.CharField('Рейтинг ресторана', max_length=10, blank=True, null=True, default=None)
    rest_image = models.ImageField(upload_to='rest_images/', blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % self.restaurant_name

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'


class Product(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, default=None)
    product_image = models.ImageField(upload_to='products_images/', blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    product_name = models.CharField('Название блюда', max_length=64, blank=True, null=True, default=None)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % self.product_name

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'


class Courier(models.Model):
    courier_name = models.CharField('Имя курьера', max_length=64, blank=True, null=True, default=None)
    courier_phone = models.CharField('Номер курьера', max_length=24, blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % self.courier_name

    class Meta:
        verbose_name = 'Курьер'
        verbose_name_plural = 'Курьеры'


class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'


class Order(models.Model):
    # courier = models.ForeignKey(Courier, on_delete=models.SET_DEFAULT)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # customer_name = models.CharField('Имя заказчика', max_length=64, blank=True, null=True, default=None)
    # customer_email = models.EmailField('Почта заказчика', blank=True, null=True, default=None)
    # customer_phone = models.CharField('Номер заказчика', max_length=12, blank=True, null=True, default=None)
    # customer_address = models.CharField('Номер заказчика', max_length=128, blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True, default=None)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'Заказ №{self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    num = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def save(self, *args, **kwargs):
        price_per_item = self.product.product_price
        self.price_per_item = price_per_item
        self.total_price = self.num * price_per_item

        super(ProductInOrder, self).save(*args, **kwargs)


def products_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)
    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price
    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)


post_save.connect(products_in_order_post_save, sender=ProductInOrder)


class ProductInBasket(models.Model):
    user_id = models.CharField(max_length=32, blank=True, null=True, default=None)
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    num = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % self.product.product_name

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        price_per_item = self.product.product_price
        self.price_per_item = price_per_item
        self.total_price = int(self.num) * price_per_item

        super(ProductInBasket, self).save(*args, **kwargs)
