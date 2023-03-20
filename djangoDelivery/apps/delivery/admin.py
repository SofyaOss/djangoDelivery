from django.contrib import admin

from .models import Restaurant, Product, Order, Courier, ProductInOrder, Status, ProductInBasket
from import_export.admin import ExportActionMixin


class ProductInOrderInline(ExportActionMixin, admin.TabularInline):
    model = ProductInOrder
    extra = 0


class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Status._meta.fields]

    class Meta:
        model = Status


class OrderAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    inlines = [ProductInOrderInline]
    list_filter = ('status',)

    class Meta:
        model = Order


class ProductInOrderAdmin (ExportActionMixin, admin.ModelAdmin):
    list_display = [field.name for field in ProductInOrder._meta.fields]

    class Meta:
        model = ProductInOrder


class ProductAdmin (ExportActionMixin, admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    list_filter = ('product_price',)

    class Meta:
        model = Product


class RestaurantAdmin (ExportActionMixin, admin.ModelAdmin):
    list_display = [field.name for field in Restaurant._meta.fields]

    class Meta:
        model = Restaurant


class CourierAdmin (ExportActionMixin, admin.ModelAdmin):
    list_display = [field.name for field in Courier._meta.fields]

    class Meta:
        model = Courier


class ProductInBasketAdmin (ExportActionMixin, admin.ModelAdmin):
    list_display = [field.name for field in ProductInBasket._meta.fields]

    class Meta:
        model = ProductInBasket


# admin.site.register(History, HistoryAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Courier, CourierAdmin)
admin.site.register(ProductInOrder, ProductInOrderAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(ProductInBasket, ProductInBasketAdmin)
