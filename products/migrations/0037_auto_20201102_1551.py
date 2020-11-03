# Generated by Django 3.1.2 on 2020-11-02 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0036_auto_20201102_0957'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created', 'name']},
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='img/no_image.png', upload_to='products/%Y/%m/%d'),
        ),
    ]
