# Generated by Django 3.1 on 2020-09-28 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20200928_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='img/no_image.png', upload_to='products/%Y/%m/%d'),
        ),
    ]