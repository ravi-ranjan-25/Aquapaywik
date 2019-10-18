# Generated by Django 2.2.1 on 2019-10-17 21:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20191016_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='complain',
            name='complaintxn',
            field=models.CharField(default='COMP123', max_length=256),
        ),
        migrations.AlterField(
            model_name='areaquantity',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 17, 21, 11, 17, 751839, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='complain',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 17, 21, 11, 17, 757481, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='housedetails',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 17, 21, 11, 17, 748955, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='quality',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 17, 21, 11, 17, 753414, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userconsumption',
            name='areaid',
            field=models.CharField(default=0, max_length=256),
        ),
        migrations.AlterField(
            model_name='userconsumption',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 17, 21, 11, 17, 754948, tzinfo=utc)),
        ),
    ]
