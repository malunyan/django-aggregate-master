# Generated by Django 4.0.5 on 2022-07-21 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myappB', '0002_alter_earnings_order_number'),
        ('myappC', '0002_alter_order3_options_alter_orderitemdetail3_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order3',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order3',
            name='code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myappB.earnings', to_field='order_number', verbose_name='注文番号'),
        ),
        migrations.AlterField(
            model_name='orderitemdetail3',
            name='code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myappB.earnings', verbose_name='注文番号'),
        ),
        migrations.AlterField(
            model_name='orderitemdetail3',
            name='key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_payment', to='myappB.earnings', verbose_name='口座情報'),
        ),
    ]
