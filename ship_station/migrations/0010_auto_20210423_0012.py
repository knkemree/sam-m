# Generated by Django 3.1.7 on 2021-04-23 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ship_station', '0009_auto_20210421_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ean',
            field=models.CharField(max_length=100, null=True),
        ),
    ]