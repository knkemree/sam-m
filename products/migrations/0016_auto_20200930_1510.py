# Generated by Django 3.1 on 2020-09-30 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20200930_1509'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='categories',
            new_name='category',
        ),
    ]
