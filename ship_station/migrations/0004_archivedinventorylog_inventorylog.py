# Generated by Django 3.1.7 on 2021-04-20 02:32

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ship_station', '0003_archivedbrand_archivedcolor_archivedmodel_archivedproduct_archivedsize_brand_color_model_product_siz'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_ts', models.DateTimeField(blank=True, editable=False, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField(default=0, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ship_station.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArchivedInventoryLog',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('ship_station.inventorylog',),
        ),
    ]
