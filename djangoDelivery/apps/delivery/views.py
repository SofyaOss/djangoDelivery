from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Restaurant, Product, ProductInBasket
from .forms import CreateUserForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .permissions import IsAdminOrReadOnly
from .serializers import RestaurantSerializer, ProdInBasketSerializer, ProductSerializer, UserSerializer, \
    PasswordSerializer


class RestsViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class ProdsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['product_name']
    ordering_fields = ['product_price']


class FilterBackend(ProdsViewSet):
    def get_filtered(self):
        prods = Product.objects.get(Q(product_price__gt=1000) & Q(restaurant__startswith='Э'))
        queryset = self.serializer_class(prods, many=True)
        return Response(queryset)


class BasketViewSet(viewsets.ModelViewSet):
    queryset = ProductInBasket.objects.all()
    serializer_class = ProdInBasketSerializer
    permission_classes = (IsAuthenticated, )

    @action(methods=['get'], detail=False)
    def prods(self, request):
        user = request.user.id
        prods = ProductInBasket.objects.filter(user_id=user)
        queryset = ProdInBasketSerializer(prods, many=True)
        return Response(queryset.data)

    @action(methods=['post'], detail=False)
    def add(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'ok'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = PasswordSerializer

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data.get['new_password'])
            user.save()
            return Response({'message': 'ok'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='register')
    def register(self, request):
        if '@' not in request.data['email']:
            raise ValidationError({'error': 'email isn\'t correct'})
        if len(request.data['login']) < 6:
            raise ValidationError({'error': 'minimum login length 6 characters'})
        if len(request.data['password']) < 6:
            raise ValidationError({'error': 'minimum password length 6 characters'})
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'ok'})


def register(request):
    if request.user.is_authenticated:
        return redirect('delivery:index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, f'Аккаунт для {user} создан!')
                return redirect('delivery:login')
        context = {'form': form}
        return render(request, 'delivery/register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('delivery:index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username,  password=password)
            if user is not None:
                login(request, user)
                return redirect('delivery:index')
            else:
                messages.info(request, 'Неверный логин или пароль')
        context = {}
        return render(request, 'delivery/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('delivery:login')


@login_required(login_url='login')
def index(request):
    # restaurant_list = Restaurant.objects.all()
    # print(Response({'rests': RestaurantSerializer(restaurant_list, many=True).data}))
    # return render(request, 'delivery/list.html', {'restaurant_list': restaurant_list})
    restaurant_list = Restaurant.objects.all()
    res = RestaurantSerializer(restaurant_list, many=True).data
    res_list = {'restaurant_list': res}
    return render(request, 'delivery/list.html', res_list)


@login_required(login_url='login')
class RestView(APIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'delivery/list.html'

    def get(self, request):
        queryset = Restaurant.objects.all()
        serialized_data = RestaurantSerializer(queryset, many=True).data
        return render(request, self.template_name, {'restaurant_list': serialized_data})
        # return render_to_response(template_name, {'data': queryset.data})
        # return Response({'restaurant_list': queryset})

    # def get(self, request):
    #     r = Restaurant.objects.all()
    #     return Response({'rests': RestaurantSerializer(r, many=True).data})


@login_required(login_url='login')
def detail(request, restaurant_id):
    try:
        rest = Restaurant.objects.get(id=restaurant_id)
    except:
        raise Http404('Ресторан не найден!')

    products_list = rest.product_set.all()
    return render(request, 'delivery/detail.html', {'restaurant': rest, 'products_list': products_list})


@login_required(login_url='login')
def info(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except:
        raise Http404('Блюдо не найдено!')

    return render(request, 'delivery/info.html', {'product': product, 'rest_id': product.restaurant})


@login_required(login_url='login')
def basket(request):
    return render(request, 'delivery/basket.html')


def basket_adding(request):
    return_dict = {}
    print('!!!')
    print(request.POST)
    data = request.POST
    product_id = data.get('product_id')
    num = data.get('num')
    user_id = request.user.id
    is_delete = data.get('is_delete')
    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(user_id=user_id,
                                                                     product_id=product_id, defaults={'num': num},
                                                                     is_active=True)
        if not created:
            new_product.num += int(num)
            new_product.save(force_update=True)

    products_total_num = ProductInBasket.objects.filter(user_id=user_id, is_active=True).count()
    return_dict['products_total_num'] = products_total_num
    print('!!!!!!', return_dict)
    return JsonResponse(return_dict)
