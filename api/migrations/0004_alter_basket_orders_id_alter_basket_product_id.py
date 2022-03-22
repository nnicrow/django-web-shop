# Generated by Django 4.0.2 on 2022-03-14 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_basket_remove_orders_product_delete_productsorders_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='orders_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.orders', verbose_name='Заказ'),
        ),
        migrations.AlterField(
            model_name='basket',
            name='product_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.products', verbose_name='Товар'),
        ),
    ]