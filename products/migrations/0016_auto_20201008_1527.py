# Generated by Django 3.1.2 on 2020-10-08 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_product_category2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='products.category2'),
        ),
    ]