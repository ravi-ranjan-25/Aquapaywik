# Generated by Django 2.2.1 on 2019-10-31 20:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20191031_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areaquantity',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 31, 20, 41, 0, 91162, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='complain',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 31, 20, 41, 0, 92522, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='housedetails',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 31, 20, 41, 0, 90520, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='quality',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 31, 20, 41, 0, 91608, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tax',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 31, 20, 41, 0, 93106, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userconsumption',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 31, 20, 41, 0, 92016, tzinfo=utc)),
        ),
    ]
