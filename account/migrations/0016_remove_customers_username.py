# Generated by Django 3.1 on 2020-09-09 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_auto_20200905_0833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customers',
            name='username',
        ),
    ]
