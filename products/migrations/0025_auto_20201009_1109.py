# Generated by Django 3.1.2 on 2020-10-09 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0024_auto_20201009_0232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category2',
        ),
        migrations.DeleteModel(
            name='Category2',
        ),
    ]