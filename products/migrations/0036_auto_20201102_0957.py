# Generated by Django 3.1.2 on 2020-11-02 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0035_auto_20201102_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='img/no_image.png', upload_to='products/%Y/%m/%d'),
            preserve_default=False,
        ),
    ]
