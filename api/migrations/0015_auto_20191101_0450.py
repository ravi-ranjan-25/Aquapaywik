# Generated by Django 2.2.1 on 2019-11-01 04:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20191101_0440'),
    ]

    operations = [
        migrations.AddField(
            model_name='complain',
            name='username',
            field=models.CharField(default='USER1', max_length=256),
        ),
        migrations.AlterField(
            model_name='areaquantity',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 1, 4, 50, 57, 747070, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='complain',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 1, 4, 50, 57, 748456, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='housedetails',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 1, 4, 50, 57, 746423, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='quality',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 1, 4, 50, 57, 747538, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tax',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 1, 4, 50, 57, 749042, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userconsumption',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 1, 4, 50, 57, 747945, tzinfo=utc)),
        ),
    ]
