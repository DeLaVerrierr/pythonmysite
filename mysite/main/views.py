from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, get_user
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .forms import RegisterUserForm, ProfileForm
from .models import UserProfile, Profile, Product, CartItem, Order, EmailAddress
import uuid
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
import requests
import codecs
import json


def index(request):
    ''' Отображает главную страницу приложения '''
    return render(request, 'main/index.html')


def lovers(request):
    ''' отображает страницу с информацией о lovers продукте с идентификатором 1 '''
    product = Product.objects.get(pk=1)
    return render(request, 'main/lovers.html', {'item': product})


def bones(request):
    ''' отображает страницу с информацией о bones продукте с идентификатором 2 '''
    product = Product.objects.get(pk=2)
    return render(request, 'main/bones.html', {'item': product})


def devil(request):
    ''' отображает страницу с информацией о devil продукте с идентификатором 3 '''
    product = Product.objects.get(pk=3)
    return render(request, 'main/devil.html', {'item': product})


def about(request):
    ''' Отображает страницу с информацией о компании '''
    return render(request, 'main/about.html')


def service(request):
    ''' Отображает страницу с информацией о предоставляемых услугах '''
    return render(request, 'main/service.html')


def contacts(request):
    ''' Отображает страницу с контактной информацией '''
    return render(request, 'main/contacts.html')


def login_user(request):
    ''' Обрабатывает запрос на вход пользователя в систему.
     Если запрос отправлен методом POST и данные формы валидны,
    производится аутентификация пользователя и перенаправление на главную страницу.
    В противном случае отображается страница входа с формой аутентификации '''
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm(request)
    return render(request, 'main/login.html', {'form': form})


class RegisterUser(CreateView):
    ''' Представляет форму регистрации пользователя.
    При валидации формы происходит сохранение нового пользователя
    и автоматический вход в систему '''
    form_class = RegisterUserForm
    template_name = 'main/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)  # Автоматический вход пользователя
        return response


class LoginUser(LoginView):
    ''' Представляет форму входа пользователя.
    После успешной аутентификации пользователь перенаправляется
    на главную страницу. '''
    template_name = 'main/login.html'
    success_url = reverse_lazy('home')


class LogoutUser(LogoutView):
    ''' Представляет функциональность выхода пользователя из системы. '''
    next_page = reverse_lazy('login')


def register(request):
    ''' Обрабатывает запрос на регистрацию пользователя.
    Если запрос отправлен методом POST и данные формы валидны,
    производится сохранение нового пользователя и автоматический вход в систему,
    после чего пользователь перенаправляется на главную страницу.
    В противном случае отображается страница регистрации с формой. '''
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход пользователя
            return redirect('home')
    else:
        form = RegisterUserForm()
    return render(request, 'main/register.html', {'form': form})


@login_required
def profile(request):
    ''' Отображает страницу профиля пользователя.
    Если запрос отправлен методом POST и данные формы валидны,
    происходит сохранение профиля пользователя.
    Если профиль уже существует, он обновляется.
    Если профиля нет, создается новый.
    После сохранения профиля пользователь перенаправляется на страницу профиля. '''
    user = request.user
    profile = user.profile if hasattr(user, 'profile') else None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user  # Set the user for the profile
            profile.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, initial={'user': user})

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'main/profile.html', context)


@login_required
def edit_profile(request):
    '''  Отображает страницу редактирования профиля пользователя.
    Если запрос отправлен методом POST и данные формы валидны, происходит сохранение профиля пользователя.
    Если профиль уже существует, он обновляется.
    Если профиля нет, создается новый.
    После сохранения профиля пользователь перенаправляется на страницу профиля. '''
    user = request.user
    profile = user.profile if hasattr(user, 'profile') else None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        if profile:
            form = ProfileForm(instance=profile)
        else:
            form = ProfileForm()

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'main/edit_profile.html', context)


def casino(request):
    ''' Отображает страницу с игрой в казино.
     Сейчас отключил'''
    return render(request, 'main/casino.html')


def add_to_cart(request, product_id):
    ''' Добавляет товар с заданным идентификатором в корзину пользователя.
    Если пользователь не авторизован, ему создается новая учетная запись и идентификатор сохраняется в сессии.
    Затем происходит добавление товара в корзину.
    Если товар уже присутствует в корзине, увеличивается его количество.
    Затем происходит перенаправление на страницу корзины. '''
    user_id = request.session.get('user_id')
    if not user_id:
        user = User.objects.create_user(username=str(uuid.uuid4()), password='')
        user_id = user.id
        request.session['user_id'] = user_id

    product = get_object_or_404(Product, pk=product_id)

    try:
        cart_item = CartItem.objects.get(product=product, user_id=user_id)
        cart_item.quantity += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem(product=product, user_id=user_id, quantity=1, price=product.price)

    cart_item.subtotal = cart_item.quantity * cart_item.price
    cart_item.save()

    return redirect('cart')


def cart(request):
    ''' Отображает страницу корзины пользователя.
    Если пользователь авторизован, отображаются все товары в его корзине.
    Иначе отображается пустая корзина. '''
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        cart_items = CartItem.objects.filter(user=user)
    else:
        cart_items = []

    total = sum(item.subtotal for item in cart_items)
    return render(request, 'main/cart.html', {'cart_items': cart_items, 'total': total})


def clear_cart(request):
    ''' Очищает корзину пользователя.
    Если пользователь не авторизован, ему создается новая учетная запись и идентификатор сохраняется в сессии.
    Затем происходит удаление всех товаров из корзины и перенаправление на страницу корзины. '''
    user_id = request.session.get('user_id')
    if not user_id:
        user = User.objects.create_user(username=str(uuid.uuid4()), password='')
        user_id = user.id
        request.session['user_id'] = user_id

    CartItem.objects.filter(user_id=user_id).delete()

    return redirect('cart')


def payment_view(request):
    ''' Отображает страницу оплаты заказа.
    Если запрос отправлен методом POST, происходит обработка данных, введенных пользователем, и создание нового объекта заказа в базе данных.
    Затем в зависимости от выбранного метода оплаты происходит отображение страницы с информацией о платеже, включая адрес доставки и итоговую сумму заказа.
    В случае выбора оплаты с помощью Mastercard отображаются дополнительные данные (номера карты).
    В случае выбора оплаты с помощью Bitcoin отображаются дополнительные данные (адрес Bitcoin и сумма в Bitcoin). '''
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address_input')
        payment_method = request.POST.get('payment_method')
        total = request.POST.get('total')
        recipient_name = request.POST.get('recipient_name')
        country = request.POST.get('country')
        street_house_apartment = request.POST.get('street_house_apartment')
        region = request.POST.get('region')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        mobile_phone = request.POST.get('mobile_phone')
        bitcoin_address = request.POST.get('bitcoin_address')
        bitcoin_amount = 0.0
        print('Адрес доставки:', shipping_address)
        print('Метод оплаты:', payment_method)
        print('Итого:', total)

        # Создание нового объекта Order и сохранение его в базе данных
        order = Order.objects.create(
            shipping_address=shipping_address,
            payment_method=payment_method,
            total=total,
            recipient_name=recipient_name,
            country=country,
            street_house_apartment=street_house_apartment,
            region=region,
            city=city,
            postal_code=postal_code,
            mobile_phone=mobile_phone,
            bitcoin_address=bitcoin_address,
            bitcoin_amount=bitcoin_amount
        )
        order.save()

        if payment_method == 'mastercard':
            mastercard_numbers = '1234 4567 8910 1112'
            total_rubles = convert_to_rubles(float(total))
            return render(request, 'main/payment.html', {
                'total': total,
                'shipping_address': shipping_address,
                'payment_method': 'Mastercard',
                'recipient_name': recipient_name,
                'country': country,
                'street_house_apartment': street_house_apartment,
                'region': region,
                'city': city,
                'postal_code': postal_code,
                'mobile_phone': mobile_phone,
                'total_rubles': total_rubles,
                'order_number': order.order_number,
                'mastercard_numbers': mastercard_numbers
            })

        elif payment_method == 'bitcoin':
            bitcoin_address = 'bc1qapp6jgy5x6ql0kn9y5chker2svwt5jzn8m8esn'
            bitcoin_amount = convert_to_bitcoin(float(total))
            return render(request, 'main/payment.html', {
                'total': total,
                'shipping_address': shipping_address,
                'payment_method': 'Bitcoin',
                'recipient_name': recipient_name,
                'country': country,
                'street_house_apartment': street_house_apartment,
                'region': region,
                'city': city,
                'postal_code': postal_code,
                'mobile_phone': mobile_phone,
                'bitcoin_address': bitcoin_address,
                'order_number': order.order_number,
                'bitcoin_amount': bitcoin_amount
            })

    return render(request, 'main/payment.html', {
        'total': total,
        'shipping_address': shipping_address,
        'payment_method': payment_method,
        'recipient_name': recipient_name,
        'country': country,
        'street_house_apartment': street_house_apartment,
        'region': region,
        'city': city,
        'postal_code': postal_code,
        'mobile_phone': mobile_phone,
        'order_number': order.order_number,
        'bitcoin_address': bitcoin_address,
        'bitcoin_amount': bitcoin_amount
    })


def convert_to_bitcoin(amount):
    ''' Выполняет конвертацию суммы из основной валюты в Bitcoin, используя текущий курс обмена. '''
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()

    if 'bitcoin' in data and 'usd' in data['bitcoin']:
        bitcoin_usd_price = data['bitcoin']['usd']
        bitcoin_amount = amount / bitcoin_usd_price
        return bitcoin_amount

    return 0.0


def convert_to_rubles(total):
    ''' Выполняет конвертацию суммы из основной валюты в рубли, используя текущий курс обмена. '''
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=usd&vs_currencies=rub'
    response = requests.get(url)
    data = response.json()

    if 'usd' in data and 'rub' in data['usd']:
        usd_rub_exchange_rate = data['usd']['rub']
        total_rubles = total * usd_rub_exchange_rate
        return round(total_rubles)

    return 0


def save_order(shipping_address, payment_method, total, recipient_name, country,
               street_house_apartment, region, city, postal_code, mobile_phone,
               bitcoin_address='', bitcoin_amount=0.0):
    ''' Создание нового объекта Order и сохранение его в базе данных '''
    order = Order.objects.create(
        shipping_address=shipping_address,
        payment_method=payment_method,
        total=total,
        recipient_name=recipient_name,
        country=country,
        street_house_apartment=street_house_apartment,
        region=region,
        city=city,
        postal_code=postal_code,
        mobile_phone=mobile_phone,
        bitcoin_address=bitcoin_address,
        bitcoin_amount=bitcoin_amount
    )
    order.save()

#В дальнешей нужно сделать эту функцию с @permission_required чтобы никто не смог открыть ее кроме тг бота или ботов к тому моменту
def get_order_info(request, order_number):
    if request.method == 'GET':
        try:
            order = Order.objects.get(order_number=order_number)
            order_info = {
                'shipping_address': order.shipping_address,
                'payment_method': order.payment_method,
                'total': int(order.total),
                'recipient_name': order.recipient_name,
                'country': order.country,
                'mobile_phone': order.mobile_phone[-4:]
            }

            devil_price = 1666
            bones_price = 2200
            lovers_price = 2500

            devil_count, bones_count, lovers_count = 0, 0, 0

            total = order_info['total']
            for i in range(total // devil_price + 1):
                for j in range(total // bones_price + 1):
                    k = (total - i * devil_price - j * bones_price) // lovers_price
                    if (i * devil_price) + (j * bones_price) + (k * lovers_price) == total:
                        devil_count, bones_count, lovers_count = i, j, k
                        break

            order_info['DEVIL'] = devil_count
            order_info['BONES'] = bones_count
            order_info['LOVERS'] = lovers_count

            return HttpResponse(json.dumps(order_info, ensure_ascii=False))
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order does not exist'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def submit_email(request):
    '''Создание модели почт для рассылки'''
    if request.method == 'POST':
        email = request.POST.get('email')
        email_address = EmailAddress(email=email)
        email_address.save()
        return redirect('home')

