# Generated by Django 3.1.7 on 2021-04-21 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ship_station', '0006_auto_20210421_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='note',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='model',
            field=models.ForeignKey(blank=True, help_text='if model is unfamiliar, search item ean at upcitemdb.com', null=True, on_delete=django.db.models.deletion.CASCADE, to='ship_station.model'),
        ),
    ]
