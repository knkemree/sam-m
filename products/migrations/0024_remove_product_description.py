# Generated by Django 3.1.2 on 2020-10-27 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_auto_20201027_1457'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
    ]