from django.contrib import admin
from .models import Profile, Product, Order,EmailAddress

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(EmailAddress)