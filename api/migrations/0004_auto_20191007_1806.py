# Generated by Django 2.2.1 on 2019-10-07 18:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20191007_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areaquantity',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 7, 18, 6, 2, 685661, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='housedetails',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 7, 18, 6, 2, 685009, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='quality',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 7, 18, 6, 2, 686103, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userconsumption',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 7, 18, 6, 2, 686488, tzinfo=utc)),
        ),
    ]
