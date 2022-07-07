# Generated by Django 3.2.9 on 2021-11-19 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20211118_2354'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterField(
            model_name='bid',
            name='bid_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='listing',
            name='start_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='created',
            field=models.DateTimeField(),
        ),
    ]
