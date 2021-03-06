# Generated by Django 4.0.2 on 2022-03-18 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_rename_orders_id_basket_order_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basket',
            options={'ordering': ['id'], 'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзина'},
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('ASSEMBLED', 'Собирается клиентом'), ('INPROCESSING', 'В обработке'), ('COMPLETED', 'Выполнен'), ('REJECTED', 'Отклонен')], default='ASSEMBLED', max_length=16, verbose_name='Способ доставки'),
        ),
    ]
