# Generated by Django 3.1.2 on 2020-10-09 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_auto_20201009_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, default='img/no_image.png', null=True, upload_to='products/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='variation',
            name='image',
            field=models.ForeignKey(blank=True, default='img/no_image.png', null=True, on_delete=django.db.models.deletion.CASCADE, to='products.productimage'),
        ),
    ]