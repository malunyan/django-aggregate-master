# Generated by Django 4.0.5 on 2022-07-22 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myappB', '0002_alter_earnings_order_number'),
        ('myappC', '0004_remove_order3_id_alter_order3_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order3',
            name='code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='myappB.earnings', to_field='order_number', verbose_name='注文番号'),
        ),
    ]
