# Generated by Django 4.0.2 on 2022-03-14 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_orders_basket_alter_basket_orders_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='orders_id',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='api.orders', verbose_name='Заказ'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='basket',
            name='product_id',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='api.products', verbose_name='Товар'),
            preserve_default=False,
        ),
    ]
