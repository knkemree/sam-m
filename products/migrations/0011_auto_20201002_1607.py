# Generated by Django 3.1 on 2020-10-02 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_product_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=3, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='variation',
            name='price',
            field=models.DecimalField(decimal_places=2, default=3, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='variation',
            name='sku',
            field=models.CharField(default='sku', max_length=60),
            preserve_default=False,
        ),
    ]