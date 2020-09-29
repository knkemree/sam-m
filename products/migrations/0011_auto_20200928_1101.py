# Generated by Django 3.1 on 2020-09-28 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20200925_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='parent_slug',
            field=models.SlugField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('slug', 'name')},
        ),
    ]