# Generated by Django 5.0.7 on 2024-07-27 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppAdmin', '0005_ads_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='lat',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ads',
            name='lng',
            field=models.IntegerField(default=0),
        ),
    ]
