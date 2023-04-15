# Generated by Django 4.1.5 on 2023-04-07 16:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CardHolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('phone', models.CharField(max_length=120)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('email', models.EmailField(blank=True, max_length=120, null=True)),
                ('card_id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True, unique=True)),
                ('qr_code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('alias', models.CharField(editable=False, max_length=8, unique=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=120, unique=True)),
                ('name', models.CharField(max_length=120)),
                ('phone', models.CharField(max_length=120)),
                ('email', models.EmailField(blank=True, max_length=120, null=True)),
                ('cardholder_commission', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10)),
                ('merchant_commission', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10)),
                ('balance', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('phone', models.CharField(max_length=120)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('email', models.EmailField(blank=True, max_length=120, null=True)),
                ('reader_id', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('wallet_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('alias', models.CharField(editable=False, max_length=8, unique=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='merchants', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_id', models.CharField(blank=True, max_length=120)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('commission_fee', models.DecimalField(decimal_places=2, default=0, max_digits=250)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('qr_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pos_api.cardholder')),
                ('wallet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos_api.merchant', to_field='wallet_id')),
            ],
        ),
    ]
