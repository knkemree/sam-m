# Generated by Django 3.1 on 2020-09-30 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20200930_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='sku',
            field=models.CharField(default='', max_length=120),
            preserve_default=False,
        ),
    ]
