# Generated by Django 4.2.15 on 2025-01-13 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_delete_order2d'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product2d',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product3d',
            name='price',
        ),
    ]
