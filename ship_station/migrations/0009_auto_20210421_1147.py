# Generated by Django 3.1.7 on 2021-04-21 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ship_station', '0008_auto_20210421_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='note',
            field=models.CharField(blank=True, help_text='type your notes here about this item', max_length=120, null=True),
        ),
    ]