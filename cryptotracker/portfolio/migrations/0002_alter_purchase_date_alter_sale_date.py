# Generated by Django 4.1.1 on 2022-10-23 14:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 10, 23, 17, 42, 39, 18941)),
        ),
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 10, 23, 17, 42, 39, 18941)),
        ),
    ]