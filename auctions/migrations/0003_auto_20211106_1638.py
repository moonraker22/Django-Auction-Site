# Generated by Django 3.2.8 on 2021-11-06 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20211106_1636'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ('-listing', '-amount'), 'verbose_name_plural': 'Bids'},
        ),
        migrations.RenameField(
            model_name='bid',
            old_name='current_bid',
            new_name='amount',
        ),
    ]
