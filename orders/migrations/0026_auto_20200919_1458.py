# Generated by Django 3.1 on 2020-09-19 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Delivery', '0001_initial'),
        ('orders', '0025_auto_20200918_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Delivery.delivery_methods'),
        ),
    ]
