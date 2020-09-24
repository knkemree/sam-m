# Generated by Django 3.1 on 2020-09-04 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('account', '0005_auto_20200904_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='groups',
            field=models.ManyToManyField(blank=True, null=True, to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='customers',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, null=True, to='auth.Permission'),
        ),
    ]
