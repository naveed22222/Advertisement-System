# Generated by Django 5.0.7 on 2024-07-28 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppAdmin', '0007_alter_ads_lat_alter_ads_lng'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ads',
            name='lat',
            field=models.TextField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='ads',
            name='lng',
            field=models.TextField(blank=True, default=0, null=True),
        ),
    ]
