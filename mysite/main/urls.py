from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name='home'),
    path('lovers/', views.lovers, name='lovers'),
    path('bones/',views.bones),
    path('devil/',views.devil),
    path('cart/', views.cart, name='cart'),
    path('about/',views.about),
    path('payment/', views.payment_view, name='payment'),
    path('contacts/',views.contacts),
    path('service/',views.service),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('get_order_info/<int:order_number>/', views.get_order_info, name='get_order_info'),
    path('casino/', views.casino, name='casino')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)