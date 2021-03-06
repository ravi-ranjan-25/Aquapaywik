# Generated by Django 2.2.1 on 2019-11-01 04:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20191031_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='consumed',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='tax',
            name='username',
            field=models.CharField(default='user1', max_length=256),
        ),
        migrations.AlterField(
            model_name='areaquantity',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 1, 4, 40, 40, 586619, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='complain',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 1, 4, 40, 40, 590621, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='housedetails',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 1, 4, 40, 40, 584770, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='quality',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 1, 4, 40, 40, 587937, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tax',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 1, 4, 40, 40, 592283, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userconsumption',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 1, 4, 40, 40, 589136, tzinfo=utc)),
        ),
    ]
