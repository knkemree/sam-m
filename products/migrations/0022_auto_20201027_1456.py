# Generated by Django 3.1.2 on 2020-10-27 19:56

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_auto_20201027_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=django_quill.fields.QuillField(blank=True, null=True),
        ),
    ]
