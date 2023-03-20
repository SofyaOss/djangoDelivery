from django.urls import path, include
from rest_framework import routers

from . import views


# router = routers.DefaultRouter()
# router.register(r'rests', views.RestsViewSet)
# router.register(r'prods', views.ProdsViewSet)
# router.register(r'basket', views.BasketViewSet)
# router.register(r'register', views.UserViewSet)

app_name = 'delivery'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:restaurant_id>/', views.detail, name='detail'),
    path('info/<int:product_id>', views.info, name='info'),
    path('basket', views.basket, name='basket'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('basket_adding/', views.basket_adding, name='basket_adding'),
    # path('api/v1/', include(router.urls)),
    # path('api/v1/auth/', include('rest_framework.urls')),
]
