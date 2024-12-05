# Generated by Django 5.0.6 on 2024-06-21 18:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateBookBorrowedHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=100)),
                ('book_price', models.IntegerField()),
                ('after_balance', models.DecimalField(decimal_places=2, max_digits=12)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
