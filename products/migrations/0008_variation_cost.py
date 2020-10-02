# Generated by Django 3.1 on 2020-10-01 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_remove_variation_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
