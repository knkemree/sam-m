# Generated by Django 3.1.2 on 2020-11-02 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0032_auto_20201030_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='img/no_image.png', null=True, upload_to='products/%Y/%m/%d'),
        ),
    ]
