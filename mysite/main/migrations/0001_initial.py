# Generated by Django 4.2.1 on 2023-06-25 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_number', models.AutoField(primary_key=True, serialize=False)),
                ('shipping_address', models.CharField(max_length=255)),
                ('payment_method', models.CharField(max_length=255)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('recipient_name', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('street_house_apartment', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=20)),
                ('mobile_phone', models.CharField(max_length=20)),
                ('bitcoin_address', models.CharField(blank=True, max_length=255, null=True)),
                ('bitcoin_amount', models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('image', models.ImageField(upload_to='products/')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('session_key', models.CharField(blank=True, max_length=40, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
