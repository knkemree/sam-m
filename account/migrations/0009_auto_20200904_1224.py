# Generated by Django 3.1 on 2020-09-04 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20200904_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='ein',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Employer Identification Number'),
        ),
    ]
