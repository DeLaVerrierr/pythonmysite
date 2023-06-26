from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('main.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    session_key = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f"CartItem {self.pk}"

class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.title




class Order(models.Model):
    order_number = models.AutoField(primary_key=True)
    shipping_address = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    recipient_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    street_house_apartment = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    mobile_phone = models.CharField(max_length=20)
    bitcoin_address = models.CharField(max_length=255, null=True, blank=True)
    bitcoin_amount = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)

