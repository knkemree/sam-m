# Generated by Django 3.1.7 on 2021-04-25 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ship_station', '0016_auto_20210425_0650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='color',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='skuID_Master',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='size',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
