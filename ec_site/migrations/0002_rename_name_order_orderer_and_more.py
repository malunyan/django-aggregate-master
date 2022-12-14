# Generated by Django 4.0.5 on 2022-06-30 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ec_site', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='name',
            new_name='orderer',
        ),
        migrations.AlterField(
            model_name='earnings',
            name='order_number',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='ec_site.order', verbose_name='注文番号'),
        ),
    ]
