# Generated by Django 4.0.2 on 2022-03-14 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_basket_orders_id_alter_basket_product_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='Basket',
        ),
        migrations.AlterField(
            model_name='basket',
            name='orders_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.orders', verbose_name='Заказ'),
        ),
        migrations.AlterField(
            model_name='basket',
            name='product_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.products', verbose_name='Товар'),
        ),
    ]
