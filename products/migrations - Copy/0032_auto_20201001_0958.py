# Generated by Django 3.1 on 2020-10-01 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0031_remove_variation_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattribute',
            name='attribute_ptr',
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='product',
        ),
        migrations.RemoveField(
            model_name='variation',
            name='image',
        ),
        migrations.RemoveField(
            model_name='variation',
            name='product',
        ),
        migrations.DeleteModel(
            name='Attribute',
        ),
        migrations.DeleteModel(
            name='AttributeBase',
        ),
        migrations.DeleteModel(
            name='ProductAttribute',
        ),
        migrations.DeleteModel(
            name='Variation',
        ),
    ]