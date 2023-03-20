from .models import ProductInBasket


def getting_basket_info(request):
    user_id = request.user.id
    products_in_basket = ProductInBasket.objects.filter(user_id=user_id, is_active=True)
    products_total_num = products_in_basket.count()
    return locals()
