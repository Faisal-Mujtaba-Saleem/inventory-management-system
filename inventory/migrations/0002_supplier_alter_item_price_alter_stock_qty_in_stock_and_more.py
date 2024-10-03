# Generated by Django 5.1.1 on 2024-10-02 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Supplier Name')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='Email')),
                ('phone', models.CharField(max_length=20, unique=True, verbose_name='Phone Number')),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.PositiveIntegerField(default=0, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='qty_in_stock',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('qty_supplied', models.PositiveIntegerField(default=0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inventory.item', verbose_name='Item')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.supplier', verbose_name='Supplier')),
            ],
        ),
    ]
