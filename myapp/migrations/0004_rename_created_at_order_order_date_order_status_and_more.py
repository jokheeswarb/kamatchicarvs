# Generated by Django 4.2.15 on 2025-01-12 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_order_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='created_at',
            new_name='order_date',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('shipped', 'Shipped')], default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='mobile_number2',
            field=models.CharField(blank=True, default=1, max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
