# Generated by Django 3.1.2 on 2020-10-22 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_variation_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='stock',
        ),
        migrations.AddField(
            model_name='variation',
            name='ecomdashid',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
