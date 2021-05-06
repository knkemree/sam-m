# Generated by Django 3.1.7 on 2021-04-26 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20210426_1319'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customers',
            old_name='is_admin',
            new_name='admin',
        ),
        migrations.RenameField(
            model_name='customers',
            old_name='is_staff',
            new_name='staff',
        ),
        migrations.AlterField(
            model_name='customers',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
    ]