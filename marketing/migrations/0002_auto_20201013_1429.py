# Generated by Django 3.1.2 on 2020-10-13 19:29

from django.db import migrations, models
import marketing.models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='image',
            field=models.ImageField(upload_to=marketing.models.slider_upload),
        ),
    ]
